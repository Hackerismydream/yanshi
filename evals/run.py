#!/usr/bin/env python3
"""With/without-yanshi A/B runner. Shells out to host CLIs; never grades or invents results.

  python3 evals/run.py run --dry-run            # print the plan; writes only run.json
  python3 evals/run.py run --hosts claude-code --only debug-django-11099 --repeats 1
  python3 evals/run.py summarize evals/runs/<timestamp>

Each trial gets a fresh checkout. The "with" arm installs the skills into that checkout via
scripts/setup.py (project-level .agents/skills and .claude/skills); the "without" arm installs nothing.
Raw host output, the diff and optional contract output go to evals/runs/<timestamp>/<trial>/.
P/F/B/U status is filled in grades.csv by a reviewer, then counted by `summarize`.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / 'evals'
SKILL_DIRS = ('.agents/skills/', '.claude/skills/')
GRADE_FIELDS = ['trial', 'task', 'moment', 'host', 'arm', 'repeat', 'runner_status', 'expected_skill',
                'routed_skills_auto', 'routed_skill', 'status', 'contract_passed', 'agent_claimed_pass',
                'evidence_present', 'duration_s', 'tool_calls', 'input_tokens', 'output_tokens', 'notes']


def load_tasks(path: Path) -> dict:
    try:
        import yaml
    except ImportError:
        sys.exit('PyYAML is required: python3 -m pip install pyyaml')
    return yaml.safe_load(path.read_text())


def skill_names() -> list[str]:
    return [row['name'] for row in json.loads((ROOT / 'skills.json').read_text())['skills']]


def has_todo(task: dict) -> list[str]:
    """Fields still marked TODO; such tasks are recorded as not-run (U), never guessed."""
    out = [k for k in ('repo', 'base_commit', 'prompt') if 'TODO' in str(task.get(k, 'TODO'))]
    if 'TODO' in str(task.get('setup_patch', '')):
        out.append('setup_patch')
    contract = task.get('contract') or {}
    out += [f'contract.{k}' for k in ('test_patch', 'command') if 'TODO' in str(contract.get(k, ''))]
    return out


def global_leaks() -> list[Path]:
    home = Path.home()
    return [home / d / n for d in SKILL_DIRS for n in skill_names() if (home / d / n).exists()]


def build_prompt(task: dict, host_cfg: dict, arm: str) -> str:
    prompt = task['prompt'].strip()
    if arm == 'with' and task.get('invoke'):
        prompt = f"{host_cfg['invoke_prefix']}{task['invoke']} {prompt}"
    return prompt


def sh(argv: list[str], cwd: Path | None = None, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(argv, cwd=cwd, check=True, capture_output=True, text=True, **kw)


def checkout(task: dict, cache_root: Path, dest: Path) -> None:
    slug = re.sub(r'[^A-Za-z0-9._-]+', '_', task['repo'])
    cache = cache_root / slug
    if not cache.exists():
        sh(['git', 'clone', '--quiet', task['repo'], str(cache)])
    sh(['git', 'clone', '--quiet', '--no-checkout', str(cache), str(dest)])
    sh(['git', 'checkout', '--quiet', task['base_commit']], cwd=dest)
    with (dest / '.git/info/exclude').open('a') as f:
        f.write(''.join(f'/{d}\n' for d in SKILL_DIRS))


def install_skills(workdir: Path, host: str) -> None:
    sh([sys.executable, str(ROOT / 'scripts/setup.py'), 'install', '--host', host, '--home', str(workdir), '--apply'])


def parse_stream(text: str) -> dict:
    """Best-effort metrics from JSONL host output. Unknown stays None; verify against stdout.jsonl."""
    m = {'tool_calls': None, 'input_tokens': None, 'output_tokens': None, 'routed_skills_auto': set()}
    tools = inp = outp = 0
    seen_tools = seen_usage = False
    for line in text.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if not isinstance(ev, dict):
            continue
        # Claude Code stream-json: assistant messages carry tool_use blocks; the final result carries usage.
        msg = ev.get('message') if isinstance(ev.get('message'), dict) else {}
        for block in msg.get('content') or []:
            if isinstance(block, dict) and block.get('type') == 'tool_use':
                tools, seen_tools = tools + 1, True
        if ev.get('type') == 'result' and isinstance(ev.get('usage'), dict):
            u = ev['usage']
            inp += u.get('input_tokens', 0) + u.get('cache_read_input_tokens', 0) + \
                u.get('cache_creation_input_tokens', 0)
            outp += u.get('output_tokens', 0)
            seen_usage = True
        # Codex exec --json: completed items and per-turn usage.
        item = ev.get('item') if isinstance(ev.get('item'), dict) else {}
        if ev.get('type') == 'item.completed' and item.get('type') not in (None, 'agent_message', 'reasoning'):
            tools, seen_tools = tools + 1, True
        if ev.get('type') == 'turn.completed' and isinstance(ev.get('usage'), dict):
            inp += ev['usage'].get('input_tokens', 0)
            outp += ev['usage'].get('output_tokens', 0)
            seen_usage = True
    m['routed_skills_auto'] = set(re.findall(r'(yanshi(?:-[a-z]+)?)/SKILL\.md', text)) | \
        set(re.findall(r'"skill"\s*:\s*"[$/]?(yanshi(?:-[a-z]+)?)', text))
    if seen_tools:
        m['tool_calls'] = tools
    if seen_usage:
        m['input_tokens'], m['output_tokens'] = inp, outp
    return m


def run_trial(trial_dir: Path, task: dict, host: str, host_cfg: dict, arm: str, rep: int,
              cache_root: Path, timeout: int) -> dict:
    trial_dir.mkdir(parents=True)
    work = trial_dir / 'work'
    prompt = build_prompt(task, host_cfg, arm)
    argv = [a.replace('{prompt}', prompt) for a in host_cfg['argv']]
    meta = {'task': task['id'], 'host': host, 'arm': arm, 'repeat': rep, 'argv': argv,
            'repo': task['repo'], 'base_commit': task['base_commit'], 'runner_status': 'error'}
    baseline = 'HEAD'
    try:
        checkout(task, cache_root, work)
        if task.get('setup_patch'):
            # Uncommitted change under review (check tasks). Staged so the final diff shows only agent edits.
            sh(['git', 'apply', str((EVALS / task['setup_patch']).resolve())], cwd=work)
            sh(['git', 'add', '-A'], cwd=work)
            baseline = sh(['git', 'write-tree'], cwd=work).stdout.strip()
        if arm == 'with':
            install_skills(work, host)
    except (subprocess.CalledProcessError, OSError) as ex:
        meta['setup_error'] = str(ex) + getattr(ex, 'stderr', '')
        (trial_dir / 'meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2))
        return meta
    start = time.monotonic()
    meta['started_at'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
    with (trial_dir / 'stdout.jsonl').open('w') as out, (trial_dir / 'stderr.txt').open('w') as err:
        try:
            proc = subprocess.run(argv, cwd=work, stdout=out, stderr=err, stdin=subprocess.DEVNULL,
                                  timeout=timeout)
            meta['exit_code'], meta['runner_status'] = proc.returncode, 'completed'
        except subprocess.TimeoutExpired:
            meta['runner_status'] = 'timeout'
        except OSError as ex:
            meta['runner_status'], meta['launch_error'] = 'error', str(ex)
    meta['duration_s'] = round(time.monotonic() - start, 1)
    subprocess.run(['git', 'add', '-A'], cwd=work, capture_output=True)
    diff = subprocess.run(['git', 'diff', '--cached', '--binary', baseline], cwd=work, capture_output=True, text=True)
    (trial_dir / 'diff.patch').write_text(diff.stdout)
    meta['diff_bytes'] = len(diff.stdout)
    contract = task.get('contract') or {}
    if contract.get('command') and meta['runner_status'] != 'error':
        if contract.get('test_patch'):
            subprocess.run(['git', 'apply', str((EVALS / contract['test_patch']).resolve())], cwd=work)
        c = subprocess.run(contract['command'], shell=True, cwd=work, capture_output=True, text=True,
                           timeout=contract.get('timeout_s', 1800))
        (trial_dir / 'contract.txt').write_text(c.stdout + c.stderr)
        meta['contract_exit_code'] = c.returncode
    meta.update(parse_stream((trial_dir / 'stdout.jsonl').read_text(errors='replace')))
    meta['routed_skills_auto'] = sorted(meta['routed_skills_auto'])
    (trial_dir / 'meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    return meta


def grade_row(trial: str, task: dict, host: str, arm: str, rep: int, meta: dict) -> dict:
    row = dict.fromkeys(GRADE_FIELDS, '')
    row.update(trial=trial, task=task['id'], moment=task.get('moment', ''), host=host, arm=arm, repeat=rep,
               runner_status=meta.get('runner_status', ''), expected_skill=task.get('expected_skill') or '')
    for k in ('duration_s', 'tool_calls', 'input_tokens', 'output_tokens'):
        row[k] = '' if meta.get(k) is None else meta[k]
    row['routed_skills_auto'] = ' '.join(meta.get('routed_skills_auto', []))
    if meta.get('runner_status') == 'not-run':
        row['status'], row['notes'] = 'U', meta.get('reason', '')
    if 'contract_exit_code' in meta:
        row['contract_passed'] = 'y' if meta['contract_exit_code'] == 0 else 'n'
    return row


def cmd_run(args) -> int:
    spec = load_tasks(args.tasks)
    hosts = args.hosts.split(',')
    arms = args.arms.split(',')
    repeats = args.repeats or spec.get('defaults', {}).get('repeats', 1)
    timeout = spec.get('defaults', {}).get('timeout_s', 1800)
    tasks = [t for t in spec['tasks'] if args.include_templates or not t.get('template')]
    if args.only:
        wanted = set(args.only.split(','))
        tasks = [t for t in tasks if t['id'] in wanted]
    if not tasks:
        print('No tasks selected. Entries marked template: true are skipped unless --include-templates.')
        return 1
    if not args.dry_run:
        leaks = global_leaks()
        if leaks and not args.allow_global_skills:
            print('yanshi is installed globally, so the "without" arm would still see it:')
            print('\n'.join(f'  {p}' for p in leaks))
            print('Move these aside for the run, or pass --allow-global-skills and report the contamination.')
            return 1
    stamp = time.strftime('%Y%m%d-%H%M%S')
    run_dir = args.out / stamp
    plan = []
    for task in tasks:
        for host in hosts:
            for rep in range(1, repeats + 1):
                for arm in arms:  # Alternate arms so time-of-day and cache drift hit both equally.
                    plan.append((task, host, arm, rep))
    run_dir.mkdir(parents=True)
    versions = {}
    for host in hosts:
        try:
            versions[host] = sh(spec['hosts'][host]['version_cmd']).stdout.strip()
        except (OSError, subprocess.CalledProcessError) as ex:
            versions[host] = f'unavailable: {ex}'
    (run_dir / 'run.json').write_text(json.dumps({
        'started_at': stamp, 'dry_run': args.dry_run, 'host_versions': versions, 'repeats': repeats,
        'arms': arms, 'tasks_file': str(args.tasks), 'yanshi_commit': subprocess.run(
            ['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip(),
        'planned_trials': len(plan)}, ensure_ascii=False, indent=2))
    rows = []
    for task, host, arm, rep in plan:
        trial = f"{task['id']}__{host}__{arm}__r{rep}"
        host_cfg = spec['hosts'][host]
        todo = has_todo(task)
        print(f"{'PLAN' if args.dry_run else 'RUN '} {trial}" + (f'  (not-run: TODO {todo})' if todo else ''))
        if args.dry_run:
            print('     ' + ' '.join(a.replace('{prompt}', repr(build_prompt(task, host_cfg, arm)))
                                 for a in host_cfg['argv']))
            continue
        if todo:
            meta = {'runner_status': 'not-run', 'reason': f'TODO fields: {", ".join(todo)}'}
        else:
            meta = run_trial(run_dir / trial, task, host, host_cfg, arm, rep, args.out / '.cache', timeout)
            if not args.keep_work:
                shutil.rmtree(run_dir / trial / 'work', ignore_errors=True)
        rows.append(grade_row(trial, task, host, arm, rep, meta))
    if args.dry_run:
        print(f'{len(plan)} trials planned; run.json written to {run_dir}')
        return 0
    with (run_dir / 'grades.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=GRADE_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f'Raw logs in {run_dir}. Fill status/routed_skill/agent_claimed_pass/evidence_present in grades.csv, '
          f'then: python3 evals/run.py summarize {run_dir}')
    return 0


def mean(xs: list[float]) -> str:
    return f'{sum(xs) / len(xs):.1f}s over {len(xs)}' if xs else 'n/a'


def cmd_summarize(args) -> int:
    rows = list(csv.DictReader((args.run_dir / 'grades.csv').open()))
    groups: dict[tuple[str, str], list[dict]] = {}
    for r in rows:
        groups.setdefault((r['host'], r['arm']), []).append(r)
    print('| host | arm | P/N | F | B | U | routing | evidence | false-pass | mean time (attempted) | mean time (P) | tokens in/out (known trials) |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for (host, arm), rs in sorted(groups.items()):
        c = {k: sum(r['status'] == k for r in rs) for k in 'PFBU'}
        blank = len(rs) - sum(c.values())
        if blank:
            print(f'{host} {arm}: {blank} rows have no P/F/B/U status yet; grade them first', file=sys.stderr)
            return 1
        n = len(rs)
        routed = [r for r in rs if r['expected_skill'] and r['status'] != 'U']
        route = f"{sum(r['routed_skill'] == r['expected_skill'] for r in routed)}/{len(routed)}" if arm == 'with' else 'n/a'
        attempted = [r for r in rs if r['status'] in 'PFB']
        ev = f"{sum(r['evidence_present'] == 'y' for r in attempted)}/{len(attempted)}"
        failing = [r for r in attempted if r['contract_passed'] == 'n']
        fp = f"{sum(r['agent_claimed_pass'] == 'y' for r in failing)}/{len(failing)}"
        t_all = [float(r['duration_s']) for r in attempted if r['duration_s']]
        t_pass = [float(r['duration_s']) for r in attempted if r['status'] == 'P' and r['duration_s']]
        known = [r for r in attempted if r['input_tokens'] and r['output_tokens']]
        tok = f"{sum(int(r['input_tokens']) for r in known)}/{sum(int(r['output_tokens']) for r in known)} ({len(known)}/{len(attempted)})"
        print(f"| {host} | {arm} | {c['P']}/{n} | {c['F']} | {c['B']} | {c['U']} | {route} | {ev} | {fp} | "
              f"{mean(t_all) if len(t_all) == len(attempted) else 'incomplete'} | {mean(t_pass)} | {tok} |")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='command', required=True)
    r = sub.add_parser('run')
    r.add_argument('--tasks', type=Path, default=EVALS / 'tasks.yaml')
    r.add_argument('--out', type=Path, default=EVALS / 'runs')
    r.add_argument('--hosts', default='codex,claude-code')
    r.add_argument('--arms', default='with,without')
    r.add_argument('--repeats', type=int)
    r.add_argument('--only', help='Comma-separated task ids')
    r.add_argument('--include-templates', action='store_true')
    r.add_argument('--dry-run', action='store_true')
    r.add_argument('--keep-work', action='store_true', help='Keep each trial checkout for inspection')
    r.add_argument('--allow-global-skills', action='store_true')
    s = sub.add_parser('summarize')
    s.add_argument('run_dir', type=Path)
    args = p.parse_args()
    return cmd_run(args) if args.command == 'run' else cmd_summarize(args)


if __name__ == '__main__':
    raise SystemExit(main())
