# 宿主适配与核对依据

核对日期：2026-10-14。外部资料仅用于宿主和安装语法，不用来补造作者的开发实践。文档支持不等于本包已做真实会话验收。

| 项目 | Codex | Claude Code |
|---|---|---|
| 用户 Skill 位置 | `~/.agents/skills/` | `~/.claude/skills/` |
| 显式选择 | `$yanshi-check` 或 Skill 选择入口 | `/yanshi-check` |
| 默认口语匹配 | name / description 与实际策略 | name / description 与实际策略 |
| 手动快捷键控制 | `agents/openai.yaml` 的 `allow_implicit_invocation: false` | frontmatter 的 `disable-model-invocation: true` |
| 项目新会话入口 | 生效的 AGENTS.md / AGENTS.override.md | CLAUDE.md 的文件导入 |

默认日常入口只使用 name 和 description。为了真正表达 Claude Code 的手动快捷键，五个快捷键增加其 frontmatter 字段；Codex 保留自己的 YAML 政策。本包不把一个宿主的开关当作跨宿主通用开关，也不绕过关闭调用的策略加载快捷键。

安装脚本按公开文档的位置复制，npx 支持同时指定 `-a codex -a claude-code`。CLI 当前 package.json 要求 Node >= 22.20.0；本包的 Python 脚本不需要 Node。

来源：
- [Codex Skills](https://developers.openai.com/codex/skills/)
- [Codex Skill 元数据](https://developers.openai.com/codex/build-skills/)
- [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md/)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Claude Code 项目记忆与导入](https://code.claude.com/docs/en/memory)
- [skills CLI](https://github.com/vercel-labs/skills)
- [Node 要求](https://github.com/vercel-labs/skills/blob/main/package.json)

当前制作环境无 codex 和 claude 可执行程序；未执行模型会话。需要完成的双宿主验收见 [host-validation.md](host-validation.md)，结果保存在 verification.md，不以文件检查代替。
