# Contributing

Issues and pull requests are welcome. Before opening a PR, run:

```bash
python3 scripts/check.py --self-test
```

## Help collect real examples

Most "真实例子 / real example" sections in [docs/author-practices.md](docs/author-practices.md) are still empty. They will only be filled with material from real sessions, never with invented stories. Useful material, redacted of secrets and internal company information:

- **Debug:** one complete troubleshooting session — the observed failure, what was checked (test output, DB state, logs, traces), the actual root cause, the fix, and how it was re-verified.
- **Check:** a case where tests were green but the business result was wrong, or where an independent review caught something the author missed.
- **Think:** a clarification exchange where the decision to stop asking and start building was made, and whether that turned out right.
- **Build:** a small change that went from a heavy workflow to direct implementation, with the self-test that caught (or missed) a problem.
- **Handoff:** a real handoff prompt and whether the next session picked up correctly.
- **Retro:** a lesson saved to `.yanshi/` and evidence that a later session actually read and applied it.
- **Thinking shortcuts (`yanshi-ask`):** a time `first`, `challenge`, `trim`, `ablate` or `boundary` changed a decision — the prompt used, the plan before, and the plan after.
- **Host routing:** transcripts from running [docs/host-validation.md](docs/host-validation.md) in Codex or Claude Code, including wrong skill selections.

For each item, include the date, the exact words used (if any), what happened, and how the result was verified. Open an issue with the material or a link to it.
