<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/yanshi-logo-transparent-128.png">
    <img src="assets/logo/yanshi-logo-transparent-ink-128.png" alt="yanshi 偃师" width="120">
  </picture>
</p>

# yanshi 偃师 · v1.1

English · [中文](README_CN.md)

**My everyday habits for building with AI. Handle simple work directly, add steps only where they help, and ground conclusions in evidence.**

The practices come from the author's [article](https://x.com/huangtongxueh/status/2108577165306687938) and [E2E post](https://x.com/huangtongxueh/status/2109687887264681986). Real session examples for each practice are still being collected — see [Help collect real examples](CONTRIBUTING.md#help-collect-real-examples).

## Moments, not a pipeline

Eight skills: six everyday moments, a manual router, and one manual skill holding five thinking shortcuts. Each works on its own.

| Skill | Say this | Invocation |
|---|---|---|
| `yanshi-think` | Help me think this through before coding | automatic or by name |
| `yanshi-debug` | Why is this failing? Help me debug it | automatic or by name |
| `yanshi-check` | Check this before I submit it; does it actually work? | automatic or by name |
| `yanshi-handoff` | Prepare a handoff for the next session | automatic or by name |
| `yanshi-retro` | Capture what went wrong and save the lesson in this project | automatic or by name |
| `yanshi-build` | Build this and self-test it | manual only |
| `yanshi` | Use yanshi to move this forward; what should we do next? | manual only |
| `yanshi-ask` | `first` / `challenge` / `trim` / `ablate` / `boundary` | manual only |

Which one: **think** before code exists; **build** when the change is decided and you want it written and self-tested; **debug** when you already see a failure and want the cause; **check** when the change is written and you want it judged against the business contract (read-only by default).

`yanshi-ask` takes an action name: in Codex `$yanshi-ask challenge this plan`, in Claude Code `/yanshi-ask trim this design`. The five actions are first principles, counterexample, Occam's razor, ablation, and responsibility boundaries. Runtime text is Chinese; descriptions are bilingual. See [usage](docs/usage.md).

## How it relates to other tools

`yanshi-check` judges whether a change meets the business contract with real evidence; a host `/code-review` looks for code defects — use both if you like. `yanshi-debug` overlaps with superpowers `systematic-debugging` and Waza `hunt`, and `yanshi-check` / `yanshi-think` overlap with Waza `check` / `think`: if you have those installed, pick one set for automatic matching to avoid routing conflicts.

## Install

With the skills CLI (requires **Node ≥ 22.20**):

```bash
npx skills add Hackerismydream/yanshi -g -a codex -y
npx skills add Hackerismydream/yanshi -g -a claude-code -y
```

Without Node, use Python ≥ 3.10. The first command previews; only `--apply` writes:

```bash
git clone https://github.com/Hackerismydream/yanshi && cd yanshi
python3 scripts/setup.py install --host both
python3 scripts/setup.py install --host both --apply
```

Existing directories cause refusal. To upgrade, add `--update`: only skills listed in `skills.json` are replaced, and existing copies are first moved to `~/.yanshi-backup/<timestamp>/`. Old pre-1.1 shortcut directories are reported, not deleted. See the [changelog](CHANGELOG.md).

## Project learning

Entries that work on a project read its `.yanshi/INDEX.md` when it exists and load only matching `active` practices. No index, no extra files. Project commands, verification entry points, and lessons belong in the project, not in the installed skills.

To have new sessions pick up the index, opt in once per project (from your clone):

```bash
python3 scripts/setup.py project --project <your-project-root>
python3 scripts/setup.py project --project <your-project-root> --apply
```

This creates an empty practice index, adds a bounded block to the root Codex instruction file (a non-empty `AGENTS.override.md` takes precedence) and `CLAUDE.md`, and adds `.yanshi/HANDOFF.md` and `.yanshi/evidence/` to the project's `.gitignore`. Existing text is preserved; rerunning changes nothing.

Retro writes only when asked to save a lesson. `candidate` entries do not apply; `active` requires a real quote, evidence, scope, and verification; outdated records become `retired`. See [project conventions](docs/project-memory.md).

## Evidence

Expected results come from the business contract. A success message does not establish persistence; verify through an independent authoritative read. API evidence does not replace required UI operations. Keep original failures across retries and repairs.

```bash
python3 scripts/check.py --self-test
```

[verification.md](verification.md) lists what these checks cover. [Practice cards](docs/author-practices.md) record when to use each practice, the author's exact words, and why; the real-example sections are mostly still empty.

## Name and sources

Yan Shi is the craftsman in *Liezi · Tang Wen* who built a mechanical performer able to sing and dance. The name evokes directing agents to do useful work.

[Design notes](design-notes.md) · [Host documentation](docs/hosts.md) · [Contributing](CONTRIBUTING.md) · [MIT](LICENSE)
