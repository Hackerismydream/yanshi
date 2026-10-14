---
name: yanshi
description: "用偃师帮我推进、看看下一步做什么 / Use yanshi to move this forward; what should we do next? 手动入口：为一个开发请求选出当前这一步。"
disable-model-invocation: true
---

# 选当前这一刻

先读 [project-context.md](project-context.md)。用一行说明当前时刻和最短动作，随后执行。

| 当前请求 | 只读这个入口 |
|---|---|
| 接到需求，影响方向或验收的问题还没想清楚 | [想清楚](../yanshi-think/SKILL.md) |
| 目标已经明确，要求写或修改实现 | [动手](../yanshi-build/SKILL.md) |
| 有报错、失败结果或“卡住了” | [排障](../yanshi-debug/SKILL.md) |
| 只要求审查、验收或提交前看一眼 | [验一下](../yanshi-check/SKILL.md) |
| 要换会话或交给另一位 Agent | [交接](../yanshi-handoff/SKILL.md) |
| 明确要求复盘、记住经验或沉淀项目规则 | [记下来](../yanshi-retro/SKILL.md) |

一个请求涉及几项时，先做阻塞当前目标的那项。用户说“只查 / 只审”时保留这个边界；仅需简单修改时直接动手并自测。

表中路径相对于本文件；能按名称调用就直接调用。思维小命令 `yanshi-ask` 由用户手动插入，这里不代跑。

结束时交代完成内容、实际证据与未验证部分。
