<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/yanshi-logo-transparent-128.png">
    <img src="assets/logo/yanshi-logo-transparent-ink-128.png" alt="yanshi 偃师" width="120">
  </picture>
</p>

<h1 align="center">yanshi 偃师</h1>

<p align="center">
  <b>我每天用 AI 开发的习惯，做成 Codex 和 Claude Code 的 8 个 Skill。</b><br>
  简单的直接做，复杂的按需加步骤，结论都有证据。
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Hackerismydream/yanshi" alt="License"></a>
  <a href="https://github.com/Hackerismydream/yanshi/stargazers"><img src="https://img.shields.io/github/stars/Hackerismydream/yanshi" alt="GitHub stars"></a>
</p>

<p align="center"><a href="README.md">English</a> · 中文</p>

## 为什么做这个

我写过一篇 [文章](https://x.com/huangtongxueh/status/2108577165306687938)，讲自己平时怎么用 AI Agent 开发；又写了一篇 [续帖](https://x.com/huangtongxueh/status/2109687887264681986)，讲怎么让 Agent 在真实产品上跑端到端测试。yanshi 把这些习惯做成 Skill，让它们在需要的时候自己出现，而不是只停留在文章里。

贯穿其中的是三件事：

- **最短有效路径。** 很多重流程在 Agent 已经掌握足够上下文之后还在继续走步骤。yanshi 没有流水线，每个 Skill 只对应一天里的一个时刻，需要哪个用哪个。
- **测试绿了不等于需求达成。** 预期结果来自业务契约，而不是系统返回了什么就认为什么是对的。成功提示不能证明数据真的落库，需求依赖的 UI 操作也不能用 API 调用代替。
- **经验留在项目里。** 在某个仓库里学到的东西，只在你要求时存进这个仓库的 `.yanshi/`，装好的 Skill 本身保持不变。

名字取自《列子·汤问》。偃师是造出能歌善舞的机关人的工匠，那个机关人逼真到周穆王把它当成了真人。这里取“指挥 Agent 干实事”之意。

每条实践的真实会话例子还在收集中，欢迎 [提供一个](CONTRIBUTING.md#help-collect-real-examples)。

## 30 秒安装

用 skills CLI（需要 **Node ≥ 22.20**）：

```bash
npx skills add Hackerismydream/yanshi -g -a codex -y
npx skills add Hackerismydream/yanshi -g -a claude-code -y
```

没有合适的 Node 时用 Python ≥ 3.10。第一条命令只预览改动，加 `--apply` 才真正写入：

```bash
git clone https://github.com/Hackerismydream/yanshi && cd yanshi
python3 scripts/setup.py install --host both
python3 scripts/setup.py install --host both --apply
```

已有同名目录时脚本会拒绝覆盖。升级时加 `--update`：只替换 `skills.json` 里列出的目录，替换前先把旧目录移到 `~/.yanshi-backup/<时间戳>/`。见 [版本记录](CHANGELOG.md)。

## 一天里怎么用

不用记 Skill 名，平时怎么说就怎么说。五个 Skill 会根据日常说法自动匹配；另外三个是手动入口，点名才运行（Codex 用 `$名称`，Claude Code 用 `/名称`）。

**9:30 · 接到需求。**
> 帮我想想怎么做，先别急着写。

`yanshi-think` 先查自己能读到的材料：需求文档、用户反馈、`CONTEXT.md` 和代码。然后只追问会改变实现方向或验收标准的问题。成熟的小改动，直接给出下一步就停。验收标准来自业务规则，不从当前实现倒推。

方案看着太重时，插入一个思维小命令：

> `/yanshi-ask trim 这个设计`

它会列出可以删掉的部分，以及删完之后仍要满足的需求。这只是建议，不会直接动代码。

**10:30 · 方案定了。**
> `/yanshi-build` 就按这个改，写完顺手测一下。

`yanshi-build` 做小范围变更，并运行从项目文档、manifest、脚本或 CI 里找到的检查。没测到的部分会直接说明。遇到原因不明的失败，它不会继续堆改动，而是保留失败信息留给排障。测试绿灯不会被当成 E2E 通过。

**14:00 · 出 bug 了。**
> 这个 bug 怎么回事，先帮我查一下。

`yanshi-debug` 把契约规定的结果和实际结果放在一起，然后用项目已有的入口复现。取证方式看失败类型：本地失败看测试输出，持久化状态查库，跨服务问题看日志或 Trace。“查一下”不等于授权修改。

**16:30 · 提交前。**
> 提交前帮我看一眼，确认真的能用。

`yanshi-check` 先看验收标准，再判断已有测试是否验证了需求真正关心的事。默认只读。需要确认真实入口和最终状态时，会沿业务路径实际操作一遍。最后列出发现、证据、未验证的风险，以及需要人来判断的问题。

**18:00 · 上下文快满了。**
> 上下文快满了，整理一下给下个会话。

`yanshi-handoff` 整理问题、范围、关键决策和验收标准，分成已完成、未验证、待继续三类。没解决的失败原样保留。你要求时，保存到 `.yanshi/HANDOFF.md`。

**18:15 · 今天踩了坑。**
> 复盘一下，把这次踩的坑记到项目里。

`yanshi-retro` 只记录实际发生的事。新条目先记为 `candidate`，有真实原话、证据、适用范围并验证过后才改为 `active`。之后的会话只读取匹配的 `active` 条目。

**随时 · 不知道下一步做什么。**
> `/yanshi` 看看下一步做什么

入口会选出当前卡住你的那一个时刻并执行。

## Skill 一览

| Skill | 时刻 | 直接这样说 | 调用方式 |
|---|---|---|---|
| [`yanshi-think`](skills/yanshi-think/SKILL.md) | 接到需求，开工前 | 帮我想想怎么做，先别急着写 | 自动或点名 |
| [`yanshi-build`](skills/yanshi-build/SKILL.md) | 目标明确，写代码 | 就按这个改，写完顺手测一下 | 仅手动 |
| [`yanshi-debug`](skills/yanshi-debug/SKILL.md) | 卡住了，出 bug | 这个 bug 怎么回事，先帮我查一下 | 自动或点名 |
| [`yanshi-check`](skills/yanshi-check/SKILL.md) | 提交、合并前 | 提交前帮我看一眼，确认真的能用 | 自动或点名 |
| [`yanshi-handoff`](skills/yanshi-handoff/SKILL.md) | 上下文满了，换会话 | 上下文快满了，整理一下给下个会话 | 自动或点名 |
| [`yanshi-retro`](skills/yanshi-retro/SKILL.md) | 需求做完，记录经验 | 复盘一下，把这次踩的坑记到项目里 | 自动或点名 |
| [`yanshi`](skills/yanshi/SKILL.md) | 不知道下一步 | 用偃师帮我推进，看看下一步做什么 | 仅手动 |
| [`yanshi-ask`](skills/yanshi-ask/SKILL.md) | 随时插入 | `first` / `challenge` / `trim` / `ablate` / `boundary` | 仅手动 |

**思维小命令。** `yanshi-ask` 一次只做一个动作，做完回到原任务：

| 动作 | 做什么 |
|---|---|
| `first` | 用第一性原理重想问题，不沿着既定方案继续设计 |
| `challenge` | 找能推翻核心假设的反例 |
| `trim` | 奥卡姆剃刀：删掉需求不需要的机制 |
| `ablate` | 设计消融实验，看收益到底来自哪个优化 |
| `boundary` | 审查职责边界，不为了拆而拆 |

Skill 正文用中文写，description 中英双语。说法和入口怎么区分，见 [使用表](docs/usage.md)。

## 项目经验

处理项目的 Skill 会读取目标项目的 `.yanshi/INDEX.md`（如果有），只加载匹配的 `active` 条目。没有索引就照常继续，不创建任何文件。要让新会话也自动接回索引，每个项目配置一次：

```bash
python3 scripts/setup.py project --project <你的项目根目录>          # 预览
python3 scripts/setup.py project --project <你的项目根目录> --apply
```

这会创建空索引，并向 Codex 入口文件和 `CLAUDE.md` 追加一段受控内容；同时把 `.yanshi/HANDOFF.md` 和 `.yanshi/evidence/` 加进 `.gitignore`。已有内容保留，重复执行不会再改动。见 [项目沉淀](docs/project-memory.md)。

## 证据与评测

目前还没有评测数字。[评测计划](docs/evaluation.md) 设计了在 Codex 和 Claude Code 上装与不装 yanshi 的 A/B 对比，任务选自公开仓库里已修复的已知问题。衡量的内容包括：日常说法能否选对入口、按业务契约判定的任务成功率、结论有没有附证据、false pass 率，以及代价。runner 骨架在 [`evals/`](evals/README.md)。有结果后会连同原始计数一起公布。

运行仓库自带的结构检查：

```bash
python3 scripts/check.py --self-test
```

检查覆盖范围见 [verification.md](verification.md)。[实践卡](docs/author-practices.md) 收录了每条实践的作者原话和背后的原因。

## 和同类项目的区别

这四个都是给编码 Agent 用的开源 Skill 集合。它们有重叠，但取舍不同。

| | yanshi | [Waza](https://github.com/tw93/Waza) | [mattpocock/skills](https://github.com/mattpocock/skills) | [superpowers](https://github.com/obra/superpowers) |
|---|---|---|---|---|
| 形态 | 8 个 Skill：5 个日常时刻、1 个入口、1 个动手入口、5 个思维小命令 | 8 个 Skill，来自 tw93 的工程习惯（`think`、`ui`、`check`、`hunt`、`write`、`learn`、`read`、`health`） | Matt Pocock 自用的 Skill，分 Engineering 和 Productivity 两类 | 一整套开发方法论 |
| 步骤怎么走 | 各自独立，需要哪个时刻用哪个 | 各自独立，附推荐的组合方式 | 每个 Skill 标注为用户调用或模型调用 | 从头脑风暴到写计划、子 Agent 开发、TDD、Review、收尾分支，README 称之为必须遵循的流程 |
| 侧重点 | 对照业务契约验收、自然语言 E2E、经验按项目沉淀 | 还覆盖 UI、写作、调研和 Agent 配置体检 | 开工前对齐与追问、TDD、让 Agent 少说废话 | 规划、测试先行和子 Agent 执行 |
| 文档覆盖的宿主 | Codex、Claude Code | Claude Code、Codex、Cursor 等 | Claude Code、Codex 等 | 很多，包括 Claude Code、Codex、Cursor、Gemini CLI |

**选 yanshi**：你的痛点不在于写出代码，而在于确认它真的完成了，并且想把经验留在仓库里。
**选 superpowers**：你想要一套从设计到合并都强制执行的完整流程。
**选 Waza 或 mattpocock/skills**：你想要覆盖面更广的个人工程习惯，包括 UI、写作和 TDD。

它们可以并存。`yanshi-debug` 与 superpowers 的 `systematic-debugging`、Waza 的 `hunt` 重叠；`yanshi-check` / `yanshi-think` 与 Waza 的 `check` / `think` 重叠。同时安装时，这几个时刻只让一套参与自动匹配。宿主自带的 `/code-review` 找代码缺陷，`yanshi-check` 判断改动是否达成需求，两者可以一起用。

## 常见问题

**yanshi 会跑固定流水线吗？**
不会。每个 Skill 都能单独用。入口 `yanshi` 只选一个时刻并执行，不会自动串联。

**`yanshi-check` 会改我的代码吗？**
默认不会。只有你要求修改时才会动代码。在真实环境执行验收前，它会先确认环境和允许的副作用。

**会往我的仓库里写东西吗？**
只有你要求时才会。`yanshi-retro` 要你说了“记到项目”才写入，`yanshi-handoff` 要你要求了才保存成文件。项目接入是一条单独的命令，而且默认先预览。

**能和 Waza 或 superpowers 一起装吗？**
可以。重叠的时刻只让一套参与自动匹配，避免宿主选得不一致。

**为什么 Skill 正文是中文？**
这是我平时的工作语言。description 是中英双语的，英文请求也能匹配到。不论哪种语言选错了入口，都欢迎 [反馈](CONTRIBUTING.md#help-collect-real-examples)。

**Cursor、Gemini CLI 等其他 Agent 能用吗？**
文档覆盖并支持的是 Codex 和 Claude Code。Skill 用的是标准 `SKILL.md` 格式，但其他宿主还没测过。

**有证据表明它有用吗？**
还没有。[评测计划](docs/evaluation.md) 就是用来产生这些证据的，结果会如实包含失败和被阻塞的运行，不只报通过。

**怎么卸载？**
从 `~/.agents/skills/` 和 `~/.claude/skills/` 删除 [`skills.json`](skills.json) 里列出的 8 个 `yanshi*` 目录。

## Star 趋势

[![Star History Chart](https://api.star-history.com/svg?repos=Hackerismydream/yanshi&type=Date)](https://star-history.com/#Hackerismydream/yanshi&Date)

## 参与贡献

欢迎提 Issue 和 PR，尤其欢迎真实会话例子：排障过程、一次“测试全绿但业务不对”被 check 拦下的经历、交接记录，以及选错入口的情况。见 [CONTRIBUTING.md](CONTRIBUTING.md)；提 PR 前先运行 `python3 scripts/check.py --self-test`。

[设计说明](design-notes.md) · [使用表](docs/usage.md) · [宿主文档依据](docs/hosts.md) · [版本记录](CHANGELOG.md) · [MIT](LICENSE)
