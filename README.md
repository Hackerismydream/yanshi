<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/yanshi-logo-transparent-128.png">
    <img src="assets/logo/yanshi-logo-transparent-ink-128.png" alt="yanshi 偃师" width="120">
  </picture>
</p>

# yanshi 偃师

English · [中文](README_CN.md)

**Challenge the design. Verify the business outcome. Hand over the evidence.**

yanshi does not wrap requirements gathering, coding, TDD, or publishing. It adds concrete counterexamples, contract-driven E2E evidence, and a handoff format for independent business-path review.

## Four skills

| Skill | Job | Implicit invocation |
|---|---|---|
| [yanshi](skills/yanshi/SKILL.md) | Identify the missing design decision, implementation, runtime evidence, or cross-review | Enabled |
| [yanshi-challenge](skills/yanshi-challenge/SKILL.md) | Challenge an untested mechanism, design an ablation, or simplify a proposal | Disabled; explicit selection or entry routing |
| [yanshi-e2e](skills/yanshi-e2e/SKILL.md) | Execute natural-language acceptance goals through real interfaces; compare execution setups | Enabled |
| [yanshi-review](skills/yanshi-review/SKILL.md) | Hand contracts and evidence to another reviewer; return findings for repair and re-verification | Disabled; explicit selection or entry routing |

The three specialist skills are independently installable. Full entry routing needs the whole suite. Runtime instructions are written in Chinese; provide task inputs in the language supported by your agent.

## Install

The skills CLI requires **Node ≥ 22.20**. Install the published suite:

```bash
npx skills add Hackerismydream/yanshi --skill '*' -g -a codex
```

Install only business-path verification:

```bash
npx skills add Hackerismydream/yanshi --skill yanshi-e2e -g -a codex
```

For an extracted or unpublished revision, run from its repository root:

```bash
npx skills add . --skill '*' -g -a codex
```

The remote command installs the published repository, not a ZIP in your working directory. For other hosts, select an agent identifier the CLI actually supports. Installer support is not evidence of tested runtime behavior.

<details>
<summary>Without Node: manual Codex installation</summary>

Run from the repository root. All destinations are checked before copying; an existing directory or symlink causes an exit rather than an overwrite.

```bash
(
  set -eu
  target="$HOME/.agents/skills"
  for name in yanshi yanshi-challenge yanshi-e2e yanshi-review; do
    test -f "skills/$name/SKILL.md"
    dest="$target/$name"
    if [ -e "$dest" ] || [ -L "$dest" ]; then
      printf 'Destination exists; back up and resolve first: %s\n' "$dest" >&2
      exit 1
    fi
  done
  mkdir -p "$target"
  for name in yanshi yanshi-challenge yanshi-e2e yanshi-review; do
    cp -R "skills/$name" "$target/$name"
  done
)
```

</details>

Before upgrading from v2, back up and remove the eight retired skill installations listed in [CHANGELOG.md](CHANGELOG.md). Replace retained skill directories as well to avoid stale references. When applying this text package to an existing repository, replace the entire `skills/` directory rather than overlaying files. Preserve existing image directories.

## Use

```text
Use yanshi-challenge on <proposal>.
Constraints: <business requirements>. Evidence: <observations>.
Find the strongest counterexample and the experiment result that would make us remove the mechanism.
```

```text
Use yanshi-e2e to verify <business outcome>, without editing code.
Contract: <location>. Entry and identity: <real environment>. Write scope: <authorization>.
Return actual actions, independent read-back, and evidence for each goal. Read existing project instructions rather than guessing commands.
```

```text
Use yanshi-review to hand <changes and evidence> to another reviewer.
Fix the contract and change snapshot first. Return concrete counterexamples to the main implementer for repair and re-verification.
```

## Evidence rules

The business contract defines expected results; tools provide evidence. A success toast does not prove persistence: use independent authoritative read-back. API results do not substitute for required UI verification. Unexecuted work is not a pass, and repairs or retries must retain the original failure.

E2E does not require a prewritten browser script or a conventional test-case suite. This is not a blanket ban on AI-written tests; code-level testing stays with the project’s existing approach.

The [comparison template](skills/yanshi-e2e/comparison-template.md) keeps P/F/B/U, fixed denominators, duration, and cost together. Unknown cost is not zero; failed samples remain in the report. The [failure-mode guide](skills/yanshi-e2e/failure-modes.md) contains diagnostic rules, not claimed production incidents.

## Hosts and dependencies

Use Codex or a host that reads standard `SKILL.md` files. No proprietary invocation tool is assumed. Frontmatter contains only `name` and `description`; Codex invocation policy lives in `agents/openai.yaml`. Hosts that ignore this metadata need their own verified invocation controls or explicit selection.

Skill icons are intentionally unset. Installing a single skill does not carry the repository-level `assets/` directory, so a repository-relative icon path would not remain reliable. README logo paths are unchanged.

There are no external skill dependencies. If you have `grilling`, `tdd`, or `code-review` installed, keep using them for their original jobs. Read their actual installed locations; do not assume sibling directories.

## Verification status

Run the package and regression checks:

```bash
python3 scripts/check.py --text-only --self-test
```

Use `--text-only` only for the text delivery without images; remove it after merging into the original repository to check image references. See [verification.md](verification.md) for results and limits. There is no host-behavior comparison or measured business improvement yet; package checks do not establish agent reliability.

## Name

Yan Shi is the craftsman in *Liezi · Tang Wen* who built a mechanical performer able to sing and dance. The name evokes directing agents to do useful work.

## Sources and design

[Original article](https://x.com/huangtongxueh/status/2108577165306687938) · [E2E post](https://x.com/huangtongxueh/status/2109687887264681986) · [Skill-writing reference](https://github.com/mattpocock/skills)

[Codex skills](https://developers.openai.com/codex/build-skills) · [skills CLI](https://github.com/vercel-labs/skills) · [CLI Node requirement](https://github.com/vercel-labs/skills/blob/main/package.json)

[design-notes.md](design-notes.md) separates source material, added design decisions, and missing field evidence. None of those provenance annotations are loaded into runtime instructions. [MIT](LICENSE).
