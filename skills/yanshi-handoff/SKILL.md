---
name: yanshi-handoff
description: "上下文快满了、整理给下个会话、交给另一个 Agent / Prepare a handoff for the next session. 用于明确的会话或执行者切换；不是发现任务复杂就自动开新会话。"
---

# 把上下文交出去

读 [project-context.md](project-context.md)，以 `[偃师·交接]` 开头说明交接对象或下一会话要继续的任务。

把这次要解决的问题、范围、关键决策、验收标准和当前进度整理成可直接接手的文本。引用已有 Spec、`CONTEXT.md`、变更及实际测试证据，不复制全部聊天。

按 [handoff-template.md](handoff-template.md) 区分已完成、未验证和需要继续处理的问题。失败还没解决就保留原失败；原话与模型建议分开。

用户要求保存时写到目标项目 `.yanshi/HANDOFF.md`，已有文件先读取再更新，不写全局 Skill 安装目录；只要一段交接 Prompt 时直接给文本。没有目标项目则不猜保存位置。

接手者重新确认版本、未提交改动、权限与证据适用范围。交接完成不等于已经启动另一位 Agent，也不代替任务完成。
