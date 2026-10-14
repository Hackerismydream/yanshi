# 日常入口与手动快捷键

以下触发句是本版交互文案，不作为作者历史原话收录。明确点名的 Skill 优先于口语匹配；宿主选错时应保留错误轨迹后修 description，而不是声称天然不会误触发。

| 时刻 / 动作 | 名称 | 中文口语 | English | 隐式匹配 |
|---|---|---|---|---|
| 不知道下一步 / 入口 | `yanshi` | 用偃师帮我推进，看看下一步做什么 | Use yanshi to move this forward; what should we do next? | 允许；受明确意图和授权限制 |
| 接到需求，开工前 / 想清楚 | `yanshi-think` | 帮我想想怎么做，先别急着写 | Help me think this through before coding | 允许；受明确意图和授权限制 |
| 目标明确，写代码 / 动手 | `yanshi-build` | 就按这个改，写完顺手测一下 | Build this and check it when you are done | 允许；受明确意图和授权限制 |
| 卡住了，出 bug / 排障 | `yanshi-debug` | 这个 bug 怎么回事，先帮我查一下 | Why is this failing? Help me debug it | 允许；受明确意图和授权限制 |
| 提交、合并前 / 验一下 | `yanshi-check` | 提交前帮我看一眼，确认真的能用 | Check this before I submit it; does it actually work? | 允许；受明确意图和授权限制 |
| 上下文满了，换会话 / 交接 | `yanshi-handoff` | 上下文快满了，整理一下给下个会话 | Prepare a handoff for the next session | 允许；受明确意图和授权限制 |
| 需求做完，记录经验 / 记下来 | `yanshi-retro` | 复盘一下，把这次踩的坑记到项目里 | Capture what went wrong and save the lesson in this project | 允许；受明确意图和授权限制 |
| 思维快捷键 / 重想问题 | `yanshi-first` | 别沿着这个方案想了，从头分析原因 | Start from first principles, not the proposed solution | 关闭；使用原生手动命令 |
| 思维快捷键 / 找反例 | `yanshi-challenge` | 别帮它找理由，找个能推翻它的反例 | Challenge this plan; find a counterexample | 关闭；使用原生手动命令 |
| 思维快捷键 / 做减法 | `yanshi-trim` | 是不是太复杂了，把不必要的删掉 | Cut the unnecessary complexity | 关闭；使用原生手动命令 |
| 思维快捷键 / 拆收益 | `yanshi-ablate` | 这几个优化，到底哪个有用 | Which of these changes actually helped? | 关闭；使用原生手动命令 |
| 思维快捷键 / 看边界 | `yanshi-boundary` | 看看职责有没有混在一起，别为了拆而拆 | Check the responsibility boundaries; do not split just to split | 关闭；使用原生手动命令 |

## 冲突怎么分

“帮我想想怎么做”是开工前讨论；“这个 bug 怎么回事”已经有失败，走 debug。“按这个改，写完测一下”属于 build；“提交前看一眼，不要改”属于 check。“复盘”只输出总结；“记到项目，下次别再犯”才允许持久化。

“用偃师推进”交给总控；直接点名入口就完成该入口，不先绕一圈总控。一般问答、文章润色、翻译不触发。纯方法讨论没有目标项目，不读取无关仓库。

## 两个宿主

Codex：`$yanshi-think 帮我想想怎么做`。
Claude Code：`/yanshi-think 帮我想想怎么做`。

五个快捷键在两个宿主都设为手动：Codex 使用 sidecar 调用策略，Claude Code 使用 `disable-model-invocation: true`。总控不靠读取被禁用的快捷键来绕过调用策略。

七个日常入口（含总控）保留口语匹配，以意图和动作边界区分，而不是延用 v3“只开两个入口”的配置。这是为自用作出的配置选择；需按 [宿主验收](host-validation.md) 检查路由混淆率，不宣称已经验证。

## 一行标识

首次实际采用入口时输出 `[偃师·<动作>] <这次怎么做>`，不要求模型暴露推理过程。读取项目索引后才可附实际读取的 active 条目数量；无索引、无项目、读取失败分别说明。一个入口同轮不重复刷标识。
