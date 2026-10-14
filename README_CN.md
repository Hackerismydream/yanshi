<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/yanshi-logo-transparent-128.png">
    <img src="assets/logo/yanshi-logo-transparent-ink-128.png" alt="yanshi 偃师" width="120">
  </picture>
</p>

# yanshi 偃师

[English](README.md) · 中文

**检查方案能否被推翻，验收结果是否真的有证据。**

yanshi 不再包办需求澄清、编码、TDD 和发布。它只补三件事：用具体反例挑战方案；按业务契约执行 E2E 并取证；把契约、变更和失败证据交给另一位审查者。

## 四个入口

| Skill | 具体用途 | 隐式触发 |
|---|---|---|
| [yanshi](skills/yanshi/SKILL.md) | 开发需求正在推进，判断下一项缺的是方案依据、实现、运行证据还是交叉审查 | 是 |
| [yanshi-challenge](skills/yanshi-challenge/SKILL.md) | 新机制有未经验证的假设；需要反例、消融或删减方案 | 否；点名或由入口选中 |
| [yanshi-e2e](skills/yanshi-e2e/SKILL.md) | 从真实入口验收自然语言目标，或比较执行组合 | 是 |
| [yanshi-review](skills/yanshi-review/SKILL.md) | 将业务契约和证据交给另一位审查者，回收发现并跟踪复验 | 否；点名或由入口选中 |

三个专业 Skill 都可独立安装。入口的完整选路需要整个套件；简单实现由当前宿主完成，不再增加转发壳。

## 安装

skills CLI 需要 **Node ≥ 22.20**。安装已发布版本：

```bash
npx skills add Hackerismydream/yanshi --skill '*' -g -a codex
```

只装业务取证：

```bash
npx skills add Hackerismydream/yanshi --skill yanshi-e2e -g -a codex
```

本地解压或尚未发布的改版，在仓库根目录运行：

```bash
npx skills add . --skill '*' -g -a codex
```

远端命令安装远端已发布内容，不会自动安装手里的 ZIP。其他宿主更换为 CLI 实际支持的 agent 标识，不把 CLI 支持误写成行为已实测。

<details>
<summary>不使用 Node：手动复制到 Codex</summary>

从仓库根目录执行；先检查全部目标，同名目录或符号链接存在即退出，不覆盖旧安装。

```bash
(
  set -eu
  target="$HOME/.agents/skills"
  for name in yanshi yanshi-challenge yanshi-e2e yanshi-review; do
    test -f "skills/$name/SKILL.md"
    dest="$target/$name"
    if [ -e "$dest" ] || [ -L "$dest" ]; then
      printf 'Destination exists; back up and resolve first: %s\n' "$dest" >&2
      exit 1
    fi
  done
  mkdir -p "$target"
  for name in yanshi yanshi-challenge yanshi-e2e yanshi-review; do
    cp -R "skills/$name" "$target/$name"
  done
)
```

</details>

从 v2 升级前，备份并移除旧安装的八个已删除入口；保留名称的 Skill 也应整体替换，避免残留参考文件。名称映射见 [CHANGELOG.md](CHANGELOG.md)。将本包用于已有仓库时，替换整个 `skills/`，不要只做覆盖解压；已有图片目录保持原样。

## 怎么用

```text
用 yanshi-challenge 审查 <方案>。
业务约束：<不能牺牲的条件>；已有证据：<观测位置>。
找最强反例，并说明什么实验结果会使你删除这个机制。
```

```text
用 yanshi-e2e 验收 <最终业务目标>，不修改代码。
契约：<条款位置>；入口与身份：<真实环境>；写入范围：<授权>。
给出实际操作、独立回读与每个目标的证据。缺少项目命令先读已有文档，不要猜。
```

```text
用 yanshi-review 把 <变更与证据> 交给另一位审查者。
先固定契约和变更快照，返回有具体反例的发现，交回主实现者修复并复验。
```

## E2E 的关键区别

预期来自业务契约，工具只提供证据。保存成功提示不证明持久化；需要独立权威回读。要求验 UI 时，API 结果不能替代 UI 通过。未执行不等于通过，修复和重试不能覆盖原失败。

不要求先生成传统测试用例或完整浏览器脚本，也不普遍禁止 AI 写测试。代码层测试继续由项目现有方式完成。

[方案对比模板](skills/yanshi-e2e/comparison-template.md) 固定 P/F/B/U 与分母，同时报告耗时和成本；未知成本不算零，失败样本不删除。[失败模式](skills/yanshi-e2e/failure-modes.md) 是排查规则，不冒充作者的事故实录。

## 宿主与依赖

以 Codex 和通用 `SKILL.md` 文件读取为入口，不要求专有调用工具。默认 frontmatter 只含 `name` 与 `description`；Codex 的隐式触发策略放在 `agents/openai.yaml`。其他宿主若忽略该元数据，需使用它实际支持的调用控制，或明确点名。

未设置 `icon_small` / `icon_large`：单个 Skill 安装不会携带仓库根目录的 `assets/`，仓库中能写出的相对路径不等于安装后仍有效。README 继续使用原有 Logo 路径。

没有外部 Skill 依赖。如果你装了 `grilling`、`tdd` 或 `code-review`，可继续用它们做原来的工作；从宿主的实际安装目录读取，不猜相邻路径。yanshi 不替它们再包一层。

## 验证状态

本次提供可运行的包结构与回归检查：

```bash
python3 scripts/check.py --text-only --self-test
```

`--text-only` 仅用于未附图片的文本交付；合回原仓库后移除该参数检查图片引用。检查结果与尚未验证的部分见 [verification.md](verification.md)。当前没有宿主行为对照或真实业务收益结论，文件检查通过不代表 Agent 变得更可靠。

## 命名由来

偃师是《列子·汤问》里造出能歌善舞的机关人的工匠，取“指挥 Agent 干活”之意。

## 来源与设计

[原文](https://x.com/huangtongxueh/status/2108577165306687938) · [E2E 帖](https://x.com/huangtongxueh/status/2109687887264681986) · [Skill 写法参考](https://github.com/mattpocock/skills)

[Codex Skill 文档](https://developers.openai.com/codex/build-skills) · [skills CLI](https://github.com/vercel-labs/skills) · [CLI 的 Node 要求](https://github.com/vercel-labs/skills/blob/main/package.json)

来源、补充设计和作者待补证据集中在 [design-notes.md](design-notes.md)，不注入运行时指令。[MIT](LICENSE)。
