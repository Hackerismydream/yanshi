<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/yanshi-logo-transparent-128.png">
    <img src="assets/logo/yanshi-logo-transparent-ink-128.png" alt="yanshi 偃师：机关人侧脸 Logo" width="120">
  </picture>
</p>

<h1 align="center">yanshi 偃师</h1>

<p align="center"><strong>按任务复杂度编排 Agent，从需求对齐到可验证交付；简单任务直接做。</strong></p>

<p align="center">
  <a href="https://github.com/Hackerismydream/yanshi/stargazers"><img src="https://img.shields.io/github/stars/Hackerismydream/yanshi?style=flat-square" alt="GitHub Stars"></a>
  <a href="https://github.com/Hackerismydream/yanshi/commits"><img src="https://img.shields.io/github/last-commit/Hackerismydream/yanshi?style=flat-square" alt="最近提交"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License"></a>
  <a href="https://x.com/huangtongxueh"><img src="https://img.shields.io/twitter/follow/huangtongxueh?style=flat-square" alt="在 X 关注 @huangtongxueh"></a>
</p>

[English](README.md) · 中文

<img src="design/images/readme-hero.png" alt="yanshi 偃师无字主题头图" width="100%">

yanshi 不是接管全流程的重框架：每一步都可跳过，已有材料和有效证据直接复用。模型能力变化后，重 Workflow 中失去收益的步骤也该删掉。唯一底线：**预期结果来自业务契约，工具只负责提供证据。**

## 何时用

总控和十个子 Skill 都是独立入口，不是强制阶段。总控按当前进度选路；单独调用子 Skill，只完成所选范围。

| Skill | 何时用 | 做什么 |
|---|---|---|
| [yanshi](skills/yanshi/SKILL.md) | 要推进一个需求，不确定下一步 | 复用材料，按复杂度选择、裁剪和推进路径 |
| [yanshi-align](skills/yanshi-align/SKILL.md) | 目标、范围或验收依据不清 | 追问影响实现的问题，明确业务契约 |
| [yanshi-design](skills/yanshi-design/SKILL.md) | 需要比较方案或验证核心假设 | 形成最小方案，用反例检查设计 |
| [yanshi-split](skills/yanshi-split/SKILL.md) | 需求较大，或有可独立推进的工作 | 拆成可独立验收的小增量，明确依赖 |
| [yanshi-implement](skills/yanshi-implement/SKILL.md) | 目标明确，已授权实现或修复 | 编码、集成并修复问题 |
| [yanshi-self-test](skills/yanshi-self-test/SKILL.md) | 需要检查代码行为或优化贡献 | 运行相关检查，按需做消融验证 |
| [yanshi-review](skills/yanshi-review/SKILL.md) | 需要第二视角审查实现或高风险改动 | 对照契约找问题，给出证据和待核实风险 |
| [yanshi-e2e](skills/yanshi-e2e/SKILL.md) | 需要确认真实业务目标能否完成 | 从实际入口操作、读取状态并取证 |
| [yanshi-accept](skills/yanshi-accept/SKILL.md) | 需要汇总证据或交给人判断 | 整理业务验收材料，标出缺口和待判断项 |
| [yanshi-handoff](skills/yanshi-handoff/SKILL.md) | 要换会话、换执行者 | 保留目标、决策、证据与下一步 |
| [yanshi-retro](skills/yanshi-retro/SKILL.md) | 有值得复用的操作或反复出现的问题 | 沉淀 SOP，删掉已无收益的约束 |

## 亮点

- **用自然语言描述 E2E 目标，在真实环境取证。** 包内提供信息查询、多轮交互、状态修改及持久化三类[目标示例](skills/yanshi-e2e/goal-examples.md)，以及[通过率、耗时和成本对比模板](skills/yanshi-e2e/comparison-template.md)。示例是虚构契约，模板不含实测成绩。
- **复用已有 Skill，也保留兜底。** 参考 mattpocock/skills 等现成 Skill 的用途，按当前环境中的实际名称委派；缺失、受限或会附带未授权动作时，执行本步的最小等效动作。
- **面向 Codex 和其他宿主。** 主文件使用通用的 `name`、`description` frontmatter；没有 Skill 调用器时，可读取文件及其参考资料执行。跨宿主适配是设计方案，各宿主实测仍在待办中。

## 安装

推荐安装命令：

```bash
npx skills add Hackerismydream/yanshi -g -a codex -y
```

使用 [vercel-labs/skills CLI](https://github.com/vercel-labs/skills)，会把全部 Skill 装到 `~/.agents/skills`（Codex 读取的用户目录）。`-a` 可换成其他[已支持的 agent](https://github.com/vercel-labs/skills#supported-agents)；只装某个子 Skill 时，追加 `--skill yanshi-e2e`。

也可以让 Agent 阅读 https://raw.githubusercontent.com/Hackerismydream/yanshi/main/llms.txt 自行安装。

<details>
<summary>手动安装到 Codex（备选）</summary>

在仓库根目录运行，将完整 Skill 目录复制到 `~/.agents/skills`：

```bash
(
  set -eu
  target="$HOME/.agents/skills"
  for src in skills/yanshi skills/yanshi-*; do
    dest="$target/$(basename "$src")"
    if [ -e "$dest" ] || [ -L "$dest" ]; then
      printf '已有同名目录，请先备份并处理：%s\n' "$dest" >&2
      exit 1
    fi
  done
  mkdir -p "$target"
  for src in skills/yanshi skills/yanshi-*; do
    cp -R "$src" "$target/$(basename "$src")"
  done
)
```

升级前处理旧安装位置中的同名 `yanshi`，避免新旧版本同时被发现。命令遇到目标目录冲突会退出，不覆盖已有文件。只安装一个子 Skill 时，复制它的完整目录即可，包括参考文件与 `agents/`。

</details>

<details>
<summary>其他宿主</summary>

把完整 Skill 目录交给当前宿主实际支持的 Skill 加载机制。未确认的宿主安装路径与调用接口不提供专属命令，也不声称完成了原生集成测试。

宿主能读取文件但没有 Skill 调用器时，可显式提供所选 `SKILL.md`，并让它按文件内指针读取同目录参考资料。这个降级方式需要文件读取能力，不等于已经实现自动发现或工具执行。

所有主文件仅使用通用 `name`、`description` frontmatter。`agents/openai.yaml` 是可选宿主元数据；不读取它的宿主仍可使用正文，但调用策略需要由宿主或使用者落实。

</details>

## 使用示例

```text
用 yanshi 推进这个需求。先复用已有材料和证据，再选最短的有效路径。
需求：<需求>
材料：<材料位置>
授权范围：<允许修改、运行和发布的范围>
```

```text
用 yanshi-e2e 验收这个功能，不改代码。
最终目标：<用户要完成的业务结果>
契约：<已确认的需求或规则>
环境：<实际入口、测试身份和证据读取能力>
```

```text
用 yanshi-review 审查当前变更，只返回有依据的问题和待核实风险。
```


各子 Skill 的 `prompts.md` 给出完整提示词，并区分原文与补充。

## 外部 Skill：可选复用，不是安装依赖

以下用途来自包内参考材料，名称和调用定位需以当前安装的 Skill 为准。包内不附第三方 Skill 源码，也不自动安装或配置它们。

| 外部 Skill | 用途 | 参考材料中的调用定位 |
|---|---|---|
| `grilling` | 需求追问 | 模型 |
| `to-spec` | 整理方案 | 用户 |
| `to-tickets` | tracer bullet 拆分 | 模型 |
| `implement` / `implement-spec` | 实现明确的任务 | 用户 |
| `tdd` | 约定 seam 上的代码层测试 | 模型 |
| `diagnosing-bugs` | 定位难缠失败和性能回退 | 模型 |
| `code-review` | 对照规范与需求审查 | 模型 |
| `handoff` | 压缩交接上下文 | 用户 |
| `retro` | 编码会话复盘 | 用户 |
| `pr` | 编写 PR 描述 | 模型 |
| `research` | 一手来源调研 | 模型 |

参考仓库：[mattpocock/skills](https://github.com/mattpocock/skills)。调用前识别当前环境的实际名称、调用政策和副作用。参考材料中的 `to-spec` 会发布到任务系统，`implement` 可能继续调用测试和审查；不能限定到本次授权和所选路径时，采用子 Skill 中的最小等效动作。

`Call the Skill tool with "<name>"` 表示按名称委派，不是终端命令。没有调用器时，可读取实际存在的对应 `SKILL.md`；外部 Skill 不随本包提供，不能假定相邻目录存在。Skill 缺失或政策不允许时执行同处的兜底，不把指令字符串当作成功调用的证据。

## E2E 的边界

输入是自然语言最终目标和每个 case 的验收目标，不要求先生成传统测试用例或完整浏览器脚本。Agent 在真实测试入口操作、读取运行状态并留下证据，稳定 SOP 可以复用；具体需求只选择适用的任务类型，不为齐全制造场景。

浏览器、API、CLI、只读数据库、日志、Trace 和 harness 按实际能力选择。需要验证 Web UI 时，API 证据不能代替 UI 通过；需要确认持久化时，成功提示不能代替独立回读。能力不足就缩小验证范围或标明阻塞，具体见[能力检查表](skills/yanshi-e2e/capabilities.md)。

代码层测试与 E2E 各取所需，不把原帖对部分项目的做法扩大为普遍禁止测试。方案对比同时呈现通过率、耗时和成本，保留失败、重试、阻塞与未运行项；没有数据就写未知，不预置排行榜。

## 宿主调用差异

总控默认由用户明确启动，子 Skill 可由 Agent 选择，也可由用户点名。调用策略通过可选宿主元数据表达；忽略元数据的宿主需要由使用者落实。

默认 frontmatter 只保留 `name` 和 `description`。如果宿主支持 `disable-model-invocation: true`，可以为只允许用户主动调用的 Skill 增加该字段；不同宿主支持程度不同，因此本套件不默认写入。

## 交付与维护

文档和证据按需要保存，已有可用材料就复用。文中的 `spec.md` 等是按需生成的运行产物，不是包内预填文件。跳过不等于通过，单独一次 E2E 通过也不等于生产环境已全面验证。

套件划分、调用适配、提示词改写、运行记录与状态等补充设计均为推断，详见[设计索引](design-notes.md)。结构检查和宿主验收边界见 [verification.md](verification.md)。

## 命名由来

偃师是《列子·汤问》中的工匠，造出能歌善舞的机关人献给周穆王。这里取“人指挥 Agent 干活”之意。

## 来源

- [原文：开发主线与业务契约原则](https://x.com/huangtongxueh/status/2108577165306687938)
- [E2E 帖：自然语言目标与真实环境取证](https://x.com/huangtongxueh/status/2109687887264681986)
- [Skill 写法参考：mattpocock/skills](https://github.com/mattpocock/skills)

补充设计索引见 [design-notes.md](design-notes.md)。

## 待办

- [ ] 演示 GIF / 截图
- [ ] 真实案例
- [ ] 各宿主实测

## License

[MIT](LICENSE)。
