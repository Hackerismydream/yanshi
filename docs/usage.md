# 日常入口与思维小命令

下面的触发句是本版的交互文案，不是作者历史原话。明确点名的 Skill 优先于口语匹配；宿主选错入口时，保留错误轨迹再修 description。

| 时刻 / 动作 | 名称 | 中文口语 | English | 隐式匹配 |
|---|---|---|---|---|
| 接到需求，开工前 / 想清楚 | `yanshi-think` | 帮我想想怎么做，先别急着写 | Help me think this through before coding | 允许 |
| 卡住了，出 bug / 排障 | `yanshi-debug` | 这个 bug 怎么回事，先帮我查一下 | Why is this failing? Help me debug it | 允许 |
| 提交、合并前 / 验一下 | `yanshi-check` | 提交前帮我看一眼，确认真的能用 | Check this before I submit it; does it actually work? | 允许 |
| 上下文满了，换会话 / 交接 | `yanshi-handoff` | 上下文快满了，整理一下给下个会话 | Prepare a handoff for the next session | 允许 |
| 需求做完，记录经验 / 记下来 | `yanshi-retro` | 复盘一下，把这次踩的坑记到项目里 | Capture what went wrong and save the lesson in this project | 允许 |
| 目标明确，写代码 / 动手 | `yanshi-build` | 就按这个改，写完顺手测一下 | Build this and self-test it | 关闭；点名调用 |
| 不知道下一步 / 入口 | `yanshi` | 用偃师帮我推进，看看下一步做什么 | Use yanshi to move this forward; what should we do next? | 关闭；点名调用 |
| 思维小命令 | `yanshi-ask` | `first` / `challenge` / `trim` / `ablate` / `boundary` | same | 关闭；点名调用 |

## yanshi-ask 的五个动作

| 动作 | 做什么 | 日常说法 |
|---|---|---|
| `first` | 重想问题 | 别沿着这个方案想了，从头分析原因 |
| `challenge` | 找反例 | 别帮它找理由，找个能推翻它的反例 |
| `trim` | 做减法 | 是不是太复杂了，把不必要的删掉 |
| `ablate` | 拆收益 | 这几个优化，到底哪个有用 |
| `boundary` | 看边界 | 看看职责有没有混在一起，别为了拆而拆 |

调用：Codex `$yanshi-ask challenge 这个方案`；Claude Code `/yanshi-ask trim 这个设计`。一次只做一个动作，不读项目上下文。

## 冲突怎么分

- **think**：还没写代码，讨论需求、范围、做法。
- **build**：方案已定，要写代码并自测。手动入口，说 `$yanshi-build` / `/yanshi-build`。
- **debug**：已经看到报错或错误结果，要找原因。“查一下”不等于授权修改。
- **check**：改动已写完，要对照业务契约审查或做真实环境验收，默认只读。
- “复盘”只输出总结；“记到项目，下次别再犯”才允许持久化。

一般问答、文章润色、翻译不触发任何入口。

## 两个宿主

Codex：`$yanshi-think 帮我想想怎么做`。
Claude Code：`/yanshi-think 帮我想想怎么做`。

手动入口在两个宿主分别配置：Codex 用 `agents/openai.yaml` 的 `allow_implicit_invocation: false`，Claude Code 用 frontmatter 的 `disable-model-invocation: true`。自动匹配的效果需按 [宿主验收](host-validation.md) 实测。

## 一行标识（可选）

首次采用入口时可以输出 `[偃师·<动作>] <这次怎么做>`。标识只说明选了哪个入口，不是完成证据。
