---
name: yanshi-handoff
description: "上下文快满了、整理给下个会话、交给另一个 Agent / Prepare a handoff for the next session. 明确要换会话或换执行者时用。"
---

# 把上下文交出去

读 [project-context.md](project-context.md)，说明交接对象或下一会话要继续的任务。

把要解决的问题、范围、关键决策、验收标准和当前进度整理成可直接接手的文本。引用已有 Spec、`CONTEXT.md`、变更和实际测试证据，而不是复制整段聊天。

按 [handoff-template.md](handoff-template.md) 区分已完成、未验证和待继续的问题。没解决的失败保留原样；用户原话与模型建议分开写。

用户要求保存时写到目标项目 `.yanshi/HANDOFF.md`，已有文件先读再更新；只要一段交接 Prompt 时直接给文本。

接手者先重新确认版本、未提交改动、权限和证据的适用范围。
