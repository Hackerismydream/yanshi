<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/yanshi-logo-transparent-128.png">
    <img src="assets/logo/yanshi-logo-transparent-ink-128.png" alt="yanshi 偃师：机关人侧脸 Logo" width="120">
  </picture>
</p>

# yanshi 偃师

按任务复杂度取用的 Agent 开发 Skill 套件。简单任务直接实现并自测；复杂任务再增加对齐、设计、拆分和审查。

**预期结果来自业务契约，工具只负责提供证据。**

这是唯一不可让步的验收原则，不是一条要求走完全部步骤的流水线。完成标准用于约束本次结论，不用于强迫执行未选步骤。

套件划分与使用约定为「推断」；来源与全部补充设计见 [design-notes.md](design-notes.md)。

## 安装

### Codex

以下安装方案为，其中目录位置经过官方文档核对。解压后，从 `yanshi-v2/` 运行：

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

官方加载位置与元数据说明：
https://x.com/huangtongxueh/status/2108577165306687938

### Grok Bot 与其他宿主

兼容方案为「推断」：把完整 Skill 目录交给当前宿主实际支持的 Skill 加载机制。材料未提供 Grok Bot 的安装路径与调用接口，本包不猜测专属命令，也不声称完成了原生集成测试。

宿主能读取文件但没有 Skill 调用器时，可显式提供所选 `SKILL.md`，并让它按文件内指针读取同目录参考资料。这个降级方式需要文件读取能力，不等于已经实现自动发现或工具执行。

所有主文件仅使用通用 `name`、`description` frontmatter。`agents/openai.yaml` 是可选宿主元数据；不读取它的宿主仍可使用正文，但调用策略需要由宿主或使用者落实。

## 子 Skill 一览

下列拆分为。所有子 Skill 都能单独使用，也能由总控调用；单独使用只完成本步，不自动接管整个需求。

| Skill | 职责 | 单独使用 | 总控调用 | 调用定位 |
|---|---|---|---|---|
| `yanshi` | 选择、推进和裁剪当前路径 | 是 | 不自调用 | 用户明确调用 |
| `yanshi-align` | 澄清目标、范围和验收 | 是 | 是 | 模型调用，也可点名 |
| `yanshi-design` | 最小方案与方案对抗审查 | 是 | 是 | 模型调用，也可点名 |
| `yanshi-split` | 拆出独立验收的小增量 | 是 | 是 | 模型调用，也可点名 |
| `yanshi-implement` | 实现、集成和修复 | 是 | 是 | 模型调用，也可点名 |
| `yanshi-self-test` | 代码层自测与优化归因 | 是 | 是 | 模型调用，也可点名 |
| `yanshi-review` | 交叉对抗性代码审查 | 是 | 是 | 模型调用，也可点名 |
| `yanshi-e2e` | 按业务目标实际操作并取证 | 是 | 是 | 模型调用，也可点名 |
| `yanshi-accept` | 整理业务验收与人工判断材料 | 是 | 是 | 模型调用，也可点名 |
| `yanshi-handoff` | 会话或执行者交接 | 是 | 是 | 模型调用，也可点名 |
| `yanshi-retro` | 复盘、沉淀 SOP、删除冗余 | 是 | 是 | 模型调用，也可点名 |

## 使用

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

这些可复制入口为。各子 Skill 的 `prompts.md` 给出完整提示词，并区分原文与补充。

## 外部 Skill：可选复用，不是安装依赖

以下用途来自附件调研；调用适配为。包内不附第三方 Skill 源码，也不自动安装或配置它们。

| 外部 Skill | 用途 | 材料中的调用定位 |
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

外部参考仓库：https://github.com/mattpocock/skills

调用前识别当前环境的实际名称、调用政策和副作用。尤其注意：材料中的 `to-spec` 会发布到任务系统，`implement` 可能继续调用测试和审查。不能限定到本次授权和所选路径时，采用子 Skill 中的最小等效动作，而不是附带执行整套外部流程。

正文中的 `Call the Skill tool with "<name>"`。没有 Skill 调用器时，读取同套件的 `../<name>/SKILL.md` 并按其执行。 表示按名称委派，不是终端命令。没有该工具、Skill 不存在或政策不允许时，执行同处的兜底；不把指令字符串当作已经成功调用。

## E2E 的边界

输入是自然语言最终目标和每个 case 的验收目标，不要求先生成传统测试用例或完整浏览器脚本。Agent 在真实测试入口操作、读取运行状态并留下证据；稳定 SOP 可以复用。

信息查询、多轮交互、状态修改及持久化三类任务都有模板示例。具体需求只选择适用类型，不为了齐全而制造场景。代码层测试与 E2E 各取所需，不把原帖对部分项目的做法扩大为普遍禁止测试。

浏览器、API、CLI、只读数据库、日志、Trace、harness 和模型均按能力选择。附件里的 ego lite、pi 仅为示例，可替换。方案对比同时呈现通过率、耗时和成本，不预置产品排行榜或模型名称。

## 交付与维护

文档和证据按需要保存；已有可用材料就复用。文中的 `spec.md` 等是按需生成的运行产物，不是包内预填文件。运行记录、缺口与状态约定为「推断」。跳过不等于通过，单独一次 E2E 通过也不等于生产环境已全面验证。

保留 `yanshi 偃师` 命名与既有品牌色，不从视觉稿反推流程。当前输入没有 Logo 二进制，本包不提供虚构图片路径、字体或重新生成的品牌素材。

本包未选择发布许可证，也未继承第三方仓库的许可证；公开发布前需确认。结构检查和宿主验收边界见 [verification.md](verification.md)。


## 宿主调用差异

默认 frontmatter 只保留 `name` 和 `description`。如果宿主支持 `disable-model-invocation: true`，可以为只允许用户主动调用的 Skill 增加该字段。不同宿主对该字段支持程度不同，因此本套件不默认写入。
