<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/yanshi-logo-transparent-128.png">
    <img src="assets/logo/yanshi-logo-transparent-ink-128.png" alt="yanshi: automaton profile logo" width="120">
  </picture>
</p>

<h1 align="center">yanshi 偃师</h1>

<p align="center"><strong>Orchestrate agents by task complexity, from requirements alignment to verifiable delivery. Handle simple tasks directly.</strong></p>

<p align="center">
  <a href="https://github.com/Hackerismydream/yanshi/stargazers"><img src="https://img.shields.io/github/stars/Hackerismydream/yanshi?style=flat-square" alt="GitHub Stars"></a>
  <a href="https://github.com/Hackerismydream/yanshi/commits"><img src="https://img.shields.io/github/last-commit/Hackerismydream/yanshi?style=flat-square" alt="Last Commit"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License"></a>
  <a href="https://x.com/huangtongxueh"><img src="https://img.shields.io/twitter/follow/huangtongxueh?style=flat-square" alt="Follow @huangtongxueh on X"></a>
</p>

English · [中文](README_CN.md)

<img src="design/images/readme-hero.png" alt="yanshi hero illustration without text" width="100%">

yanshi is not a heavyweight framework that takes over the entire workflow: every step can be skipped, and existing materials and valid evidence can be reused directly. As model capabilities change, steps in a heavy workflow that no longer pay off should be removed. One rule remains: **expected outcomes come from the business contract; tools only provide evidence.**

## When to Use

The orchestrator and ten sub-skills are independent entry points, not mandatory stages. The orchestrator chooses a path based on current progress; calling a sub-skill directly limits work to that scope.

| Skill | When to use it | What it does |
|---|---|---|
| [yanshi](skills/yanshi/SKILL.md) | You want to move a requirement forward but are unsure of the next step | Reuses materials and selects, trims, and follows a path based on complexity |
| [yanshi-align](skills/yanshi-align/SKILL.md) | Goals, scope, or acceptance criteria are unclear | Asks questions that affect implementation and clarifies the business contract |
| [yanshi-design](skills/yanshi-design/SKILL.md) | You need to compare approaches or validate core assumptions | Develops a minimal design and checks it against counterexamples |
| [yanshi-split](skills/yanshi-split/SKILL.md) | The requirement is large or includes independently actionable work | Splits work into independently verifiable increments and identifies dependencies |
| [yanshi-implement](skills/yanshi-implement/SKILL.md) | The goal is clear and implementation or fixes are authorized | Writes code, integrates changes, and fixes problems |
| [yanshi-self-test](skills/yanshi-self-test/SKILL.md) | You need to check code behavior or an optimization's contribution | Runs relevant checks and ablation experiments as needed |
| [yanshi-review](skills/yanshi-review/SKILL.md) | You need a second perspective on an implementation or high-risk change | Checks against the contract and reports evidence-backed issues and risks to verify |
| [yanshi-e2e](skills/yanshi-e2e/SKILL.md) | You need to confirm that a real business goal can be completed | Operates through the actual entry point, reads state, and collects evidence |
| [yanshi-accept](skills/yanshi-accept/SKILL.md) | You need to consolidate evidence or hand it to a person for judgment | Prepares business acceptance materials and flags gaps and pending decisions |
| [yanshi-handoff](skills/yanshi-handoff/SKILL.md) | You are switching sessions or executors | Preserves goals, decisions, evidence, and next steps |
| [yanshi-retro](skills/yanshi-retro/SKILL.md) | An operation is worth reusing or a problem keeps recurring | Records SOPs and removes constraints that no longer help |

## Highlights

- **Describe E2E goals in natural language and collect evidence in a real environment.** The package includes [goal examples](skills/yanshi-e2e/goal-examples.md) in three categories: information retrieval, multi-turn interaction, and state changes with persistence. It also provides a [comparison template for pass rate, duration, and cost](skills/yanshi-e2e/comparison-template.md). The examples are fictional contracts; the template contains no measured results.
- **Reuse existing skills with a fallback.** Use the roles of existing skills, such as those in mattpocock/skills, as references and delegate by their actual names in the current environment. If a skill is missing, restricted, or would perform unauthorized actions, carry out the smallest equivalent action for that step.
- **Designed for Codex and other hosts.** Main files use generic `name` and `description` frontmatter. Without a skill invocation tool, an agent can read the files and their references to follow the instructions. Cross-host adaptation is a design proposal; testing on individual hosts remains on the TODO list.

## Installation

Recommended installation command:

```bash
npx skills add Hackerismydream/yanshi -g -a codex -y
```

This uses the [vercel-labs/skills CLI](https://github.com/vercel-labs/skills) to install all skills into `~/.agents/skills`, the user directory read by Codex. Change `-a` to another [supported agent](https://github.com/vercel-labs/skills#supported-agents); to install only one sub-skill, append `--skill yanshi-e2e`.

You can also ask your agent to read https://raw.githubusercontent.com/Hackerismydream/yanshi/main/llms.txt and install the skills itself.

<details>
<summary>Manual installation for Codex (alternative)</summary>

Run this from the repository root to copy the complete skill directories into `~/.agents/skills`:

```bash
(
  set -eu
  target="$HOME/.agents/skills"
  for src in skills/yanshi skills/yanshi-*; do
    dest="$target/$(basename "$src")"
    if [ -e "$dest" ] || [ -L "$dest" ]; then
      printf '已有同名目录，请先备份并处理：%s\n' "$dest" >&2
      exit 1
    fi
  done
  mkdir -p "$target"
  for src in skills/yanshi skills/yanshi-*; do
    cp -R "$src" "$target/$(basename "$src")"
  done
)
```

Before upgrading, resolve any existing `yanshi` directory in an older installation location so both versions are not discovered at once. The command exits on a destination conflict without overwriting existing files. To install only one sub-skill, copy its complete directory, including reference files and `agents/`.

</details>

<details>
<summary>Other hosts</summary>

Pass the complete skill directories to the skill loading mechanism actually supported by your host. No host-specific commands are provided for unconfirmed installation paths or invocation interfaces, and no native integration testing is claimed.

If the host can read files but has no skill invocation tool, provide the selected `SKILL.md` explicitly and ask it to follow the pointers to reference materials in the same directory. This fallback requires file-reading capability; it does not establish automatic discovery or tool execution.

All main files use only generic `name` and `description` frontmatter. `agents/openai.yaml` is optional host metadata. Hosts that do not read it can still use the body, but invocation policy must be enforced by the host or user.

</details>

## Usage Examples

```text
Use yanshi to move this requirement forward. Reuse existing materials and evidence first, then choose the shortest effective path.
Requirement: <requirement>
Materials: <material locations>
Authorized scope: <allowed changes, execution, and publishing>
```

```text
Use yanshi-e2e to verify acceptance of this feature without changing code.
Final goal: <business outcome the user wants to achieve>
Contract: <confirmed requirements or rules>
Environment: <actual entry point, test identity, and evidence-reading capabilities>
```

```text
Use yanshi-review to review the current changes. Return only evidence-backed issues and risks that still need verification.
```

Each sub-skill's `prompts.md` provides full prompts and distinguishes original text from additions.

## External Skills: Optional Reuse, Not Installation Dependencies

The roles below come from the package's reference materials. Names and invocation roles must be checked against the skills currently installed. This package does not bundle third-party skill source code or automatically install or configure those skills.

| External skill | Purpose | Invocation role in the reference materials |
|---|---|---|
| `grilling` | Clarify requirements | Model |
| `to-spec` | Document a design | User |
| `to-tickets` | Split work into tracer bullets | Model |
| `implement` / `implement-spec` | Implement a well-defined task | User |
| `tdd` | Code-level testing at agreed seams | Model |
| `diagnosing-bugs` | Diagnose stubborn failures and performance regressions | Model |
| `code-review` | Review against specifications and requirements | Model |
| `handoff` | Compress context for a handoff | User |
| `retro` | Reflect on a coding session | User |
| `pr` | Write PR descriptions | Model |
| `research` | Research primary sources | Model |

Reference repository: [mattpocock/skills](https://github.com/mattpocock/skills). Before invoking a skill, identify its actual name, invocation policy, and side effects in the current environment. In the reference materials, `to-spec` publishes to a task system, and `implement` may invoke testing and review. If these actions cannot be limited to the current authorization and selected path, use the sub-skill's smallest equivalent action.

`Call the Skill tool with "<name>"` means delegation by name, not a terminal command. Without an invocation tool, read the corresponding `SKILL.md` if it actually exists. External skills are not included in this package; do not assume they exist in adjacent directories. If a skill is missing or policy prevents its use, follow the fallback provided alongside the instruction. An instruction string is not evidence of a successful invocation.

## E2E Boundaries

Inputs are a natural-language final goal and acceptance goals for each case. There is no requirement to generate traditional test cases or a complete browser script first. The agent operates through real test entry points, reads runtime state, and records evidence; stable SOPs can be reused. Select only task types relevant to the requirement, without inventing scenarios for completeness.

Choose browsers, APIs, CLIs, read-only databases, logs, traces, and harnesses according to actual capabilities. When verifying a Web UI, API evidence cannot substitute for a UI pass. When confirming persistence, a success message cannot substitute for an independent readback. If capabilities are insufficient, narrow the verification scope or mark the blocker. See the [capability checklist](skills/yanshi-e2e/capabilities.md).

Use code-level tests and E2E where each is useful; do not turn the original post's approach for some projects into a universal ban on tests. Compare pass rate, duration, and cost together, retaining failures, retries, blocked cases, and cases not run. Without data, report unknowns rather than inventing rankings.

## Host Invocation Differences

By default, the orchestrator is explicitly started by the user. Sub-skills may be selected by an agent or named by the user. Invocation policy is expressed through optional host metadata; users must enforce it on hosts that ignore the metadata.

Default frontmatter contains only `name` and `description`. If a host supports `disable-model-invocation: true`, that field can be added to skills intended for explicit user invocation only. Support varies by host, so this suite does not include it by default.

## Delivery and Maintenance

Save documents and evidence as needed, reusing existing materials when available. Files such as `spec.md` mentioned in the text are runtime artifacts generated as needed, not prefilled files in the package. Skipped does not mean passed, and a single E2E pass does not mean the entire production environment has been verified.

Supplementary designs for the suite's structure, invocation adaptation, prompt rewrites, run records, and status are inferred extensions. See the [design index](design-notes.md). For structural checks and host acceptance boundaries, see [verification.md](verification.md).

## Naming

Yan Shi (偃师) is an artisan in the Liezi "Tang Wen" chapter who built a singing and dancing automaton for King Mu of Zhou. Here, the name conveys the idea of people directing agents to do work.

## Sources

- [Original post: development workflow and business contract principles](https://x.com/huangtongxueh/status/2108577165306687938)
- [E2E post: natural-language goals and evidence from real environments](https://x.com/huangtongxueh/status/2109687887264681986)
- [Skill writing reference: mattpocock/skills](https://github.com/mattpocock/skills)

See [design-notes.md](design-notes.md) for the supplementary design index.

## TODO

- [ ] Demo GIF / screenshots
- [ ] Real-world cases
- [ ] Testing on individual hosts

## License

[MIT](LICENSE).
