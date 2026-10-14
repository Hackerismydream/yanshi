# 宿主适配与核对依据

核对日期：2026-10-14。外部资料仅用于宿主和安装语法。

| 项目 | Codex | Claude Code |
|---|---|---|
| 用户 Skill 位置 | `~/.agents/skills/` | `~/.claude/skills/` |
| 显式选择 | `$yanshi-check` 或 Skill 选择入口 | `/yanshi-check` |
| 默认口语匹配 | name / description 与实际策略 | name / description 与实际策略 |
| 手动入口控制 | `agents/openai.yaml` 的 `allow_implicit_invocation: false` | frontmatter 的 `disable-model-invocation: true` |
| 项目新会话入口 | 生效的 AGENTS.md / AGENTS.override.md | CLAUDE.md 的文件导入 |

自动匹配的入口只使用 name 和 description。`yanshi`、`yanshi-build`、`yanshi-ask` 是手动入口，两个宿主的开关分别配置，`check.py` 核对两边与 `skills.json` 一致。

安装脚本按公开文档的位置复制；skills CLI 用 `-a codex` / `-a claude-code` 选择宿主，当前 package.json 要求 Node >= 22.20.0。Python 脚本不需要 Node。

来源：
- [Codex Skills](https://developers.openai.com/codex/skills/)
- [Codex Skill 元数据](https://developers.openai.com/codex/build-skills/)
- [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md/)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Claude Code 项目记忆与导入](https://code.claude.com/docs/en/memory)
- [skills CLI](https://github.com/vercel-labs/skills)
- [Node 要求](https://github.com/vercel-labs/skills/blob/main/package.json)

真实模型会话尚未执行。双宿主验收步骤见 [host-validation.md](host-validation.md)，结果记录在 [host-results.json](../verification/host-results.json)。
