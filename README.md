<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/yanshi-logo-transparent-128.png">
    <img src="assets/logo/yanshi-logo-transparent-ink-128.png" alt="yanshi 偃师" width="120">
  </picture>
</p>

# yanshi 偃师 · v1.0

English · [中文](README_CN.md)

**My everyday habits for building with AI. Handle simple work directly, add steps only where they help, and ground conclusions in evidence.**

An author-use build, not a claim of proven improvement. Practice content comes from the author's supplied article, E2E post, and actual correction records. Missing real examples remain empty. Entry names, storage conventions, and host integration are implementation decisions rather than historical practice claims.

## Moments, not a pipeline

Six everyday entries cover thinking before starting, building and checking the change, debugging a failure, checking before submission, handing off, and reflecting. `yanshi` selects the current moment. Five manual shortcuts preserve the author's concise thinking prompts. Each specialist works on its own; full routing requires the whole suite.

| Entry | Say this |
|---|---|
| `yanshi` | Use yanshi to move this forward; what should we do next? |
| `yanshi-think` | Help me think this through before coding |
| `yanshi-build` | Build this and check it when you are done |
| `yanshi-debug` | Why is this failing? Help me debug it |
| `yanshi-check` | Check this before I submit it; does it actually work? |
| `yanshi-handoff` | Prepare a handoff for the next session |
| `yanshi-retro` | Capture what went wrong and save the lesson in this project |
| `yanshi-first` | Start from first principles, not the proposed solution |
| `yanshi-challenge` | Challenge this plan; find a counterexample |
| `yanshi-trim` | Cut the unnecessary complexity |
| `yanshi-ablate` | Which of these changes actually helped? |
| `yanshi-boundary` | Check the responsibility boundaries; do not split just to split |

In Codex, use `$yanshi-challenge`; in Claude Code, use `/yanshi-challenge`. The other names work the same way. The five shortcuts are manual-only and are not five additional stages. Runtime text is Chinese; trigger descriptions include both languages. See [usage](docs/usage.md).

## Install

The skills CLI requires **Node ≥ 22.20**. To try this local package, run from its extracted root:

```bash
npx skills add . --skill '*' -g -a codex -a claude-code
```

After this revision is published:

```bash
npx skills add Hackerismydream/yanshi --skill '*' -g -a codex -a claude-code
```

Replace `'*'` with one skill name for a single entry. The remote command installs the remote repository, not an unpublished local ZIP.

Without a suitable Node installation, use Python ≥ 3.10 and the included copy script. The first command previews; only `--apply` writes:

```bash
python3 scripts/setup.py install --host both
python3 scripts/setup.py install --host both --apply
```

All destinations are checked first. Existing directories and dangling symlinks cause refusal, not overwrite. Follow [migration notes](CHANGELOG.md) rather than clearing your global skills. Codex sidecar policy and Claude Code frontmatter controls are configured separately; copied files alone do not prove host execution.

## Project learning

Every entry reads the target project's `.yanshi/INDEX.md` when it exists and loads only matching `active` practices. No index means no extra files are created for a small task. Project commands, verification entry points, and actual lessons belong in the project, not in the installed generic skills.

To reconnect the index at the start of new sessions, opt in once from the target project root:

```bash
python3 /actual/package/path/yanshi-v1.0/scripts/setup.py project --project .
python3 /actual/package/path/yanshi-v1.0/scripts/setup.py project --project . --apply
```

This creates an empty practice index and adds a bounded block to the effective root Codex instruction file and `CLAUDE.md`, preserving existing text. A non-empty `AGENTS.override.md` takes precedence. The script does not change global configuration. It is an optional setup action, not a new task stage.

Retro writes only when asked to save a lesson. `candidate` entries do not automatically apply; `active` requires a real quote, evidence, scope, and verification; outdated records become `retired`. Reading is driven by host instructions and skill file access, not a background process or guaranteed model behavior. See [project conventions](docs/project-memory.md).

The first progress line identifies the selected entry, such as `[偃师·排障]`. Any reported count of loaded project practices must reflect actual reads. A banner is not acceptance evidence.

## Evidence and validation

Expected results come from the business contract. A success message does not establish persistence; verify through an independent authoritative read. API evidence does not replace required UI operations. Keep original failures across retries and repairs. E2E does not require a prewritten browser script; this is not a blanket ban on AI-written tests.

```bash
python3 scripts/check.py --self-test
```

See [verification.md](verification.md) for package checks, script tests, and unexecuted host tests. Live Codex and Claude Code sessions have not been validated here. The [local Codex task](docs/codex-task.md) covers real-host checks without treating output markers as proof.

Each [practice card](docs/author-practices.md) separates when to use it, the author's exact words, the actual reason or failure, and a real example. [Missing evidence](docs/author-evidence-request.md) stays visibly missing.

## Name, logo, and sources

Yan Shi is the craftsman in *Liezi · Tang Wen* who built a mechanical performer able to sing and dance. The name evokes directing agents to do useful work. The existing light/dark README logo paths are retained; per-skill icons are unset because single-skill installs do not include repository assets.

[Article](https://x.com/huangtongxueh/status/2108577165306687938) · [E2E post](https://x.com/huangtongxueh/status/2109687887264681986) · [Design and source boundaries](design-notes.md) · [Host documentation](docs/hosts.md)

[MIT](LICENSE). Version `1.0.0` names this product iteration, not a completed field-validation claim.
