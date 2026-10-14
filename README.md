<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/yanshi-logo-transparent-128.png">
    <img src="assets/logo/yanshi-logo-transparent-ink-128.png" alt="yanshi 偃师" width="120">
  </picture>
</p>

<h1 align="center">yanshi 偃师</h1>

<p align="center">
  <b>My everyday habits for building with AI, as eight skills for Codex and Claude Code.</b><br>
  Handle simple work directly, add steps only where they help, and back every conclusion with evidence.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Hackerismydream/yanshi" alt="License"></a>
  <a href="https://github.com/Hackerismydream/yanshi/stargazers"><img src="https://img.shields.io/github/stars/Hackerismydream/yanshi" alt="GitHub stars"></a>
</p>

<p align="center">English · <a href="README_CN.md">中文</a></p>

## Why

I wrote [an article](https://x.com/huangtongxueh/status/2108577165306687938) about how I actually build software with AI agents, and [a follow-up](https://x.com/huangtongxueh/status/2109687887264681986) on having agents run end-to-end tests against the real product. yanshi turns those habits into skills, so they kick in when you need them instead of only living in a post.

Three ideas run through all of it:

- **The shortest useful path.** Heavy workflows often keep running steps after the agent already has enough context. So yanshi has no pipeline. Each skill covers one moment in the day, and you use only the one you need.
- **Green tests are not a met requirement.** Expected results come from the business contract, not from whatever the system returned. A success toast doesn't prove anything was saved, and API calls don't replace the UI steps the requirement depends on.
- **Lessons belong to the project.** What you learn in a repo gets saved in that repo's `.yanshi/`, and only when you ask. The installed skills stay the same.

The name comes from *Liezi · Tang Wen*. Yan Shi (偃师) was the artisan who built an automaton so lifelike it could sing and dance, and the king took it for a person. Here it means directing agents to do real work.

Real session examples for each practice are still being collected. [Share one](CONTRIBUTING.md#help-collect-real-examples).

## Install in 30 seconds

With the skills CLI (requires **Node ≥ 22.20**):

```bash
npx skills add Hackerismydream/yanshi -g -a codex -y
npx skills add Hackerismydream/yanshi -g -a claude-code -y
```

Without Node, use Python ≥ 3.10. The first command only previews the changes. Nothing is written until you add `--apply`:

```bash
git clone https://github.com/Hackerismydream/yanshi && cd yanshi
python3 scripts/setup.py install --host both
python3 scripts/setup.py install --host both --apply
```

The script refuses to overwrite existing directories. To upgrade, add `--update`. It replaces only the skills listed in `skills.json` and first moves the old copies to `~/.yanshi-backup/<timestamp>/`. See the [changelog](CHANGELOG.md).

## What a day looks like

You don't have to remember skill names. Ask the way you normally would. Five skills match everyday phrasing on their own. Three are manual and run only when you name them (`$name` in Codex, `/name` in Claude Code).

**9:30 · A requirement lands.**
> Help me think this through before coding.

`yanshi-think` first checks the materials it can read: requirement docs, feedback, `CONTEXT.md`, and code. It then asks only the questions that would change the direction or the acceptance criteria. For a mature, small change, it gives you the next step and stops. Acceptance criteria come from business rules and are never reverse-engineered from the current implementation.

If the design looks over-built, ask for a single thinking shortcut:

> `/yanshi-ask trim this design`

It lists what to cut and what still has to hold once those parts are gone. It suggests the cuts but doesn't apply them.

**10:30 · The plan is settled.**
> `/yanshi-build` Build this and self-test it.

`yanshi-build` makes a small, scoped change and runs the checks it finds in the project's docs, manifests, scripts, or CI. If it couldn't test something, it says so. If a failure has no clear cause, it stops piling on changes and keeps the failure for debugging. It never presents green tests as an end-to-end pass.

**14:00 · Something breaks.**
> Why is this failing? Help me debug it.

`yanshi-debug` puts what the contract requires next to what actually happened, then reproduces the problem through the project's own entry points. How it gathers evidence depends on the failure: test output for local failures, the database for persisted state, logs or traces across services. "Look into it" is not permission to edit.

**16:30 · Before you submit.**
> Check this before I submit it; does it actually work?

`yanshi-check` reads the acceptance criteria first and asks whether the tests verify what the requirement actually cares about. It is read-only by default. When the real entry point and final state matter, it runs the business path for real. It ends with findings, evidence, unverified risks, and the questions only a person can answer.

**18:00 · Context is nearly full.**
> Prepare a handoff for the next session.

`yanshi-handoff` writes down the problem, the scope, key decisions, and the acceptance criteria, sorted into done, unverified, and still open. Unresolved failures stay as they were. If you ask, it saves everything to `.yanshi/HANDOFF.md`.

**18:15 · Something went wrong today.**
> Capture what went wrong and save the lesson in this project.

`yanshi-retro` records only what actually happened. A new entry starts as `candidate`. It becomes `active` only once it has a real quote, evidence, a scope, and has been verified. Future sessions read the matching `active` entries.

**Anytime · Not sure what's next?**
> `/yanshi` what should we do next?

The router picks the single moment that is blocking you and runs it.

## Skills

| Skill | Moment | Say this | Invocation |
|---|---|---|---|
| [`yanshi-think`](skills/yanshi-think/SKILL.md) | Before code exists | Help me think this through before coding | automatic or by name |
| [`yanshi-build`](skills/yanshi-build/SKILL.md) | Plan settled, write it | Build this and self-test it | manual only |
| [`yanshi-debug`](skills/yanshi-debug/SKILL.md) | You see a failure | Why is this failing? Help me debug it | automatic or by name |
| [`yanshi-check`](skills/yanshi-check/SKILL.md) | Before submit or merge | Check this before I submit it; does it actually work? | automatic or by name |
| [`yanshi-handoff`](skills/yanshi-handoff/SKILL.md) | Switching session or agent | Prepare a handoff for the next session | automatic or by name |
| [`yanshi-retro`](skills/yanshi-retro/SKILL.md) | Work done, keep the lesson | Capture what went wrong and save the lesson in this project | automatic or by name |
| [`yanshi`](skills/yanshi/SKILL.md) | Not sure what's next | Use yanshi to move this forward; what should we do next? | manual only |
| [`yanshi-ask`](skills/yanshi-ask/SKILL.md) | Anytime | `first` / `challenge` / `trim` / `ablate` / `boundary` | manual only |

**Thinking shortcuts.** `yanshi-ask` runs exactly one action and then returns to the task:

| Action | What it does |
|---|---|
| `first` | Rethink the problem from first principles instead of building on the chosen fix |
| `challenge` | Look for a counterexample that breaks the core assumption |
| `trim` | Occam's razor: drop every mechanism the requirement doesn't need |
| `ablate` | Design an ablation to find which optimization actually helps |
| `boundary` | Review responsibility boundaries without splitting for the sake of it |

Skill bodies are written in Chinese, and every description is bilingual. See the [usage guide](docs/usage.md) for phrasing and for how to tell the moments apart.

## Project learning

Skills that work on a project read its `.yanshi/INDEX.md` if there is one, and load only the matching `active` practices. With no index, they create nothing. To have new sessions pick up the index, opt in once per project:

```bash
python3 scripts/setup.py project --project <your-project-root>          # preview
python3 scripts/setup.py project --project <your-project-root> --apply
```

This creates an empty index and adds a bounded block to the Codex instruction file and to `CLAUDE.md`. It also adds `.yanshi/HANDOFF.md` and `.yanshi/evidence/` to `.gitignore`. Existing text is preserved, and running it again changes nothing. See [project conventions](docs/project-memory.md).

## Evidence and evaluation

There are no benchmark numbers yet. The [evaluation plan](docs/evaluation.md) describes a with-versus-without A/B test on Codex and Claude Code, built on public repos with known, already-fixed bugs. It measures whether skill routing works from everyday phrasing, task success judged by the business contract, whether evidence is present, the false-pass rate, and cost. The runner skeleton lives in [`evals/`](evals/README.md). Results will be published with their raw counts once they exist.

To run the repository's own structural checks:

```bash
python3 scripts/check.py --self-test
```

[verification.md](verification.md) lists what those checks cover. The [practice cards](docs/author-practices.md) give my exact words and the reasoning behind each practice.

## How it compares

All four projects are open-source skill collections for coding agents. They overlap in places but make different bets.

| | yanshi | [Waza](https://github.com/tw93/Waza) | [mattpocock/skills](https://github.com/mattpocock/skills) | [superpowers](https://github.com/obra/superpowers) |
|---|---|---|---|---|
| Shape | 8 skills: 5 daily moments, a router, a build entry, 5 thinking shortcuts | 8 skills from tw93's engineering habits (`think`, `ui`, `check`, `hunt`, `write`, `learn`, `read`, `health`) | Matt Pocock's personal skills, grouped into Engineering and Productivity | A complete development methodology |
| How steps run | Independent; you use the one moment you need | Independent skills, with suggested chains | Each skill is marked user-invoked or model-invoked | Workflow from brainstorming to plans, subagent-driven development, TDD, review, and finishing the branch, described as mandatory |
| Distinctive focus | Checking against the business contract, natural-language E2E, lessons stored per project | Also covers UI, writing, research, and auditing your agent setup | Alignment and grilling before coding, TDD, keeping agents terse | Planning, test-first discipline, and running subagents |
| Hosts documented | Codex, Claude Code | Claude Code, Codex, Cursor, and more | Claude Code, Codex, and more | Many, including Claude Code, Codex, Cursor, and Gemini CLI |

**Pick yanshi** if your problem is less about producing code and more about knowing whether it's done, and you want lessons kept in the repo.
**Pick superpowers** if you want a full, opinionated process enforced from design to merge.
**Pick Waza or mattpocock/skills** if you want a broader set of personal engineering habits, including UI, writing, and TDD.

They can coexist. `yanshi-debug` overlaps with superpowers `systematic-debugging` and Waza `hunt`, and `yanshi-check` and `yanshi-think` overlap with Waza `check` and `think`. If you install both, let only one set match automatically for those moments. A host's own `/code-review` looks for code defects, while `yanshi-check` asks whether the change meets the requirement, so using both is fine.

## FAQ

**Does yanshi run a fixed pipeline?**
No. Each skill stands alone. The `yanshi` router picks one moment and runs it, and nothing chains automatically.

**Will `yanshi-check` modify my code?**
Not by default. It is read-only unless you ask for changes. Before running acceptance steps against an environment, it confirms which side effects are allowed.

**Does anything get written to my repo?**
Only when you ask. `yanshi-retro` writes only after you say to save the lesson, and `yanshi-handoff` saves to a file only on request. Project opt-in is a separate command that previews its changes first.

**Can I use it alongside Waza or superpowers?**
Yes. For the overlapping moments, let one set handle automatic matching so the host doesn't pick inconsistently.

**Why are the skill bodies in Chinese?**
They come from my own working language. Descriptions are bilingual so English requests can match too. If routing goes wrong in either language, please [report it](CONTRIBUTING.md#help-collect-real-examples).

**Does it work in Cursor, Gemini CLI, or other agents?**
Codex and Claude Code are the documented and supported targets. The skills use the standard `SKILL.md` format, but other hosts haven't been tested.

**Is there evidence that it helps?**
Not yet. The [evaluation plan](docs/evaluation.md) is how that evidence will be produced, and it will include failures and blocked runs as well as passes.

**How do I uninstall?**
Delete the eight `yanshi*` directories listed in [`skills.json`](skills.json) from `~/.agents/skills/` and `~/.claude/skills/`.

## Star history

[![Star History Chart](https://api.star-history.com/svg?repos=Hackerismydream/yanshi&type=Date)](https://star-history.com/#Hackerismydream/yanshi&Date)

## Contributing

Issues and pull requests are welcome. Real session examples are especially welcome: debugging sessions, checks that caught a green-but-wrong change, handoffs, and routing mistakes. See [CONTRIBUTING.md](CONTRIBUTING.md), and run `python3 scripts/check.py --self-test` before opening a PR.

[Design notes](design-notes.md) · [Usage](docs/usage.md) · [Host documentation](docs/hosts.md) · [Changelog](CHANGELOG.md) · [MIT](LICENSE)
