#!/usr/bin/env python3
"""Check this package's narrow format and regressions; never infer model behavior."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ['README.md','README_CN.md','llms.txt','LICENSE','VERSION','CHANGELOG.md',
            'design-notes.md','verification.md','skills.json','scripts/setup.py',
            'scripts/test_setup.py','docs/usage.md','docs/project-memory.md',
            'docs/author-practices.md','docs/source-excerpts.json','docs/author-evidence-request.md',
            'docs/host-validation.md','docs/codex-task.md','docs/hosts.md']
IMAGES = {'assets/logo/yanshi-logo-transparent-128.png':'280655e979e8503a99495084db3dd17eafb9028f',
          'assets/logo/yanshi-logo-transparent-ink-128.png':'5f59805ff19c572ab8642fc66a67e6cdc5184801'}
NOISE = re.compile(r'推断|\bP[01]\d\b|Call the Skill tool|article\.md|e2e-post\.md|matt-skills\.md|来源见 README')
DAMAGE = re.compile(r'。。|，；|[：；]。|(?:字段|规则|场景|设计|整理|格式)(?:全部|均)?为。')
LINK = re.compile(r'\[[^\]\n]*\]\(([^\s)]+)\)')
HTML = re.compile(r'(?:src|srcset|href)="([^"\s]+)"')


def manifest(text: str) -> dict:
    match = re.fullmatch(r'---\nname: ([a-z0-9-]+)\ndescription: ("[^\n]*")\n(disable-model-invocation: true\n)?---\n[\s\S]+', text)
    if not match:
        raise ValueError('invalid package frontmatter format')
    return {'name':match[1], 'description':json.loads(match[2]), 'manual':bool(match[3])}


def audit(root: Path, text_only: bool = False) -> list[str]:
    root = root.resolve()
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f'missing {name}')
    try:
        data = json.loads((root / 'skills.json').read_text())
        rows = data['skills']
        names = [r['name'] for r in rows]
        if len(names) != 12 or len(set(names)) != 12:
            errors.append('catalog requires exactly 12 unique skill names')
        if data['version'] != (root / 'VERSION').read_text().strip():
            errors.append('version mismatch')
        actual = {p.name for p in (root / 'skills').iterdir() if p.is_dir()}
        if actual != set(names):
            errors.append('skill directory set differs from catalog')
        shared = set()
        for row in rows:
            n = row['name']
            directory = root / 'skills' / n
            text = (directory / 'SKILL.md').read_text()
            m = manifest(text)
            if m['name'] != n or m['manual'] == row['implicit']:
                errors.append(f'{n}: name or invocation policy mismatch')
            if not re.search(r'[\u4e00-\u9fff]', m['description']) or not re.search(r'[A-Za-z]{3}',m['description']):
                errors.append(f'{n}: missing bilingual description')
            if '[偃师·' not in text or '[project-context.md](project-context.md)' not in text:
                errors.append(f'{n}: missing activation marker or project read')
            meta = (directory / 'agents/openai.yaml').read_text()
            fields = re.fullmatch(r'interface:\n  display_name: ("[^\n]*")\n  short_description: ("[^\n]*")\n  brand_color: "#[0-9a-fA-F]{6}"\npolicy:\n  allow_implicit_invocation: (true|false)\n',meta)
            if not fields or ((fields[3] == 'true') != row['implicit']):
                errors.append(f'{n}: invalid metadata or cross-host policy mismatch')
            elif not all(json.loads(fields[i]).strip() for i in (1,2)):
                errors.append(f'{n}: empty interface text')
            shared.add((directory / 'project-context.md').read_bytes())
        if len(shared) != 1:
            errors.append('project-context copies differ')
        for file in ['README.md','README_CN.md','llms.txt','docs/usage.md']:
            text = (root / file).read_text()
            if any(n not in text for n in names):
                errors.append(f'{file}: stale skill list')
        for file in ['README.md','README_CN.md','llms.txt']:
            if '22.20' not in (root / file).read_text():
                errors.append(f'{file}: missing Node requirement')
    except (OSError,ValueError,KeyError,TypeError) as ex:
        errors.append(f'catalog/skill validation: {ex}')
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if '.git' in rel.parts or '__pycache__' in rel.parts:
            continue
        if path.is_symlink():
            errors.append(f'package contains symlink: {rel}')
            continue
        if not path.is_file() or path.suffix not in {'.md','.txt','.yaml'}:
            continue
        try:
            text = path.read_text()
        except (UnicodeError,OSError) as ex:
            errors.append(f'{rel}: {ex}')
            continue
        runtime = rel.parts[0] == 'skills'
        if runtime and NOISE.search(text):
            errors.append(f'{rel}: runtime provenance noise or proprietary invocation')
        if DAMAGE.search(text):
            errors.append(f'{rel}: damaged punctuation/sentence')
        fence = None
        for line in text.splitlines():
            opening = re.match(r'^(`{3,}|~{3,})(.*)$',line)
            if opening:
                ticks,rest = opening.groups()
                if fence is None:
                    fence = ticks
                elif ticks[0] == fence[0] and len(ticks) >= len(fence) and not rest.strip():
                    fence = None
        if fence:
            errors.append(f'{rel}: unclosed fence')
        for link in LINK.findall(text) + HTML.findall(text):
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            dest = (path.parent / unquote(parsed.path)).resolve()
            if not dest.is_relative_to(root):
                errors.append(f'{rel}: escaping link {link}')
                continue
            dest_rel = dest.relative_to(root).as_posix()
            if not dest.exists() and not (text_only and dest_rel in IMAGES):
                errors.append(f'{rel}: missing link {link}')
            if runtime and rel.parts[1] != 'yanshi' and not dest.is_relative_to(root / 'skills' / rel.parts[1]):
                errors.append(f'{rel}: specialist depends on another skill')
    for name, expected in IMAGES.items():
        p = root / name
        if not p.exists() and text_only:
            continue
        if not p.is_file():
            errors.append(f'missing preserved logo: {name}')
        else:
            blob = p.read_bytes()
            sha = hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()
            if sha != expected:
                errors.append(f'logo changed: {name}')
    for p in (root / 'skills/yanshi-retro').glob('*template.md'):
        if p.name == 'practice-template.md':
            text=p.read_text()
            for heading in ['什么时候用','作者原话','为什么（踩过的坑）','真实例子']:
                if f'## {heading}' not in text:
                    errors.append(f'practice template missing {heading}')
    try:
        excerpts=json.loads((root/'docs/source-excerpts.json').read_text())
        cards=(root/'docs/author-practices.md').read_text()
        if any(x['author_quote'] not in cards for x in excerpts):
            errors.append('practice card quote differs from source excerpt')
    except (OSError,ValueError,KeyError) as ex:
        errors.append(f'source mapping: {ex}')
    return errors


def mutation_test(root: Path) -> int:
    cases = [
        ('runtime label','skills/yanshi-debug/SKILL.md','append','\n（推断）\n'),
        ('numbered label','skills/yanshi-debug/SKILL.md','append','\nP'+'01\n'),
        ('double punctuation','skills/yanshi-check/SKILL.md','append','\n完成。。\n'),
        ('damaged sentence','skills/yanshi-check/SKILL.md','append','\n字段为。\n'),
        ('missing local link','skills/yanshi-debug/SKILL.md','append','\n[x](missing.md)\n'),
        ('invented sibling','skills/yanshi-debug/SKILL.md','append','\n[x](../tdd/SKILL.md)\n'),
        ('proprietary invocation','skills/yanshi-check/SKILL.md','append','\nCall the Skill tool\n'),
        ('missing project reference','skills/yanshi-build/project-context.md','delete',''),
        ('wrong skill name','skills/yanshi-build/SKILL.md','replace','name: yanshi-build\0name: wrong'),
        ('wrong manual flag','skills/yanshi-first/SKILL.md','replace','disable-model-invocation: true\n\0'),
        ('wrong sidecar','skills/yanshi-first/agents/openai.yaml','replace','invocation: false\0invocation: true'),
        ('stale README','README.md','replace','yanshi-debug\0legacy-debug'),
        ('Node requirement','llms.txt','replace','22.20\0unspecified'),
        ('unclosed fence','skills/yanshi-check/SKILL.md','append','\n```text\n'),
        ('divergent context','skills/yanshi-debug/project-context.md','append','\nextra\n'),
        ('missing four-part field','skills/yanshi-retro/practice-template.md','replace','## 作者原话\0## 代写引语'),
        ('unknown image','README.md','append','\n<img src="assets/logo/missing.png">\n'),
        ('source quote changed','docs/source-excerpts.json','replace','简单任务直接做\0先把所有步骤走完'),
    ]
    for label,relative,action,value in cases:
        with tempfile.TemporaryDirectory(prefix='yanshi-mutation-') as tmp:
            copy=Path(tmp)/'package'
            shutil.copytree(root,copy,ignore=shutil.ignore_patterns('.git','__pycache__'))
            p=copy/relative
            if action=='delete':
                p.unlink()
            else:
                text=p.read_text()
                if action=='append':
                    text+=value
                else:
                    before,after=value.split('\0')
                    if before not in text:
                        raise ValueError(f'mutation anchor missing: {label}')
                    text=text.replace(before,after,1)
                p.write_text(text)
            if not audit(copy,True):
                raise ValueError(f'undetected mutation: {label}')
            print(f'PASS detect: {label}')
    return len(cases)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--text-only',action='store_true',help='Permit only known preserved logos to be absent')
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    try:
        errors=audit(args.root,args.text_only)
        if errors:
            print('\n'.join('FAIL '+x for x in errors));return 1
        print('PASS package, bilingual catalog, host policies, references, source quote mapping, preserved logos')
        if args.self_test:
            print(f'PASS mutation checks: {mutation_test(args.root)}')
            run=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(args.root/'scripts'),'-p','test_*.py','-v'],
                               cwd=args.root,check=False)
            if run.returncode:
                return run.returncode
        print('Scope: packaging and setup only; host model sessions and business outcomes are not established.')
        return 0
    except (OSError,ValueError,KeyError,TypeError) as ex:
        print(f'FAIL {ex}');return 1

if __name__=='__main__':
    raise SystemExit(main())
