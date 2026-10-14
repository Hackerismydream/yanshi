<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/yanshi-logo-transparent-128.png">
    <img src="assets/logo/yanshi-logo-transparent-ink-128.png" alt="yanshi 偃师" width="120">
  </picture>
</p>

# yanshi 偃师 · v1.1

[English](README.md) · 中文

**我每天用 AI 开发的习惯。简单的直接做，复杂的按需加步骤，结论都有证据。**

实践来自作者的 [原文](https://x.com/huangtongxueh/status/2108577165306687938) 和 [E2E 帖](https://x.com/huangtongxueh/status/2109687887264681986)。每条实践的真实会话例子还在收集中，见 [帮忙收集真实例子](CONTRIBUTING.md#help-collect-real-examples)。

## 一天里自然用起来

| 当前时刻 | 入口 | 直接这样说 | 调用方式 |
|---|---|---|---|
| 接到需求，开工前 | [yanshi-think](skills/yanshi-think/SKILL.md) | 帮我想想怎么做，先别急着写 | 自动或点名 |
| 卡住了，出 bug | [yanshi-debug](skills/yanshi-debug/SKILL.md) | 这个 bug 怎么回事，先帮我查一下 | 自动或点名 |
| 提交、合并前 | [yanshi-check](skills/yanshi-check/SKILL.md) | 提交前帮我看一眼，确认真的能用 | 自动或点名 |
| 上下文满了，换会话 | [yanshi-handoff](skills/yanshi-handoff/SKILL.md) | 上下文快满了，整理一下给下个会话 | 自动或点名 |
| 需求做完，记录经验 | [yanshi-retro](skills/yanshi-retro/SKILL.md) | 复盘一下，把这次踩的坑记到项目里 | 自动或点名 |
| 目标明确，写代码 | [yanshi-build](skills/yanshi-build/SKILL.md) | 就按这个改，写完顺手测一下 | 仅手动 |
| 不知道下一步 | [yanshi](skills/yanshi/SKILL.md) | 用偃师帮我推进，看看下一步做什么 | 仅手动 |

怎么分：还没写代码、要想清楚做法用 **think**；方案已定、要动手写并自测用 **build**；已经看到失败、要找原因用 **debug**；改动已写完、要对照业务契约判断是否真的达成（默认只读）用 **check**。

## 五个随时插入的小命令：yanshi-ask

| 动作 | 做什么 | 日常说法 |
|---|---|---|
| `first` | 重想问题 | 别沿着这个方案想了，从头分析原因 |
| `challenge` | 找反例 | 别帮它找理由，找个能推翻它的反例 |
| `trim` | 做减法 | 是不是太复杂了，把不必要的删掉 |
| `ablate` | 拆收益 | 这几个优化，到底哪个有用 |
| `boundary` | 看边界 | 看看职责有没有混在一起，别为了拆而拆 |

Codex 用 `$yanshi-ask challenge 这个方案`，Claude Code 用 `/yanshi-ask trim 这个设计`。只能手动调用，一次只做一个动作。详见 [使用表](docs/usage.md)。

## 和其他工具的关系

`yanshi-check` 对照业务契约、用真实证据判断改动是否达成需求；宿主自带的 `/code-review` 找代码缺陷，两者可以同时用。`yanshi-debug` 与 superpowers 的 `systematic-debugging`、Waza 的 `hunt` 重叠，`yanshi-check` / `yanshi-think` 与 Waza 的 `check` / `think` 重叠：同时安装时，建议只让一套参与自动匹配，避免选错入口。

## 安装到 Codex 和 Claude Code

用 skills CLI（需要 **Node ≥ 22.20**）：

```bash
npx skills add Hackerismydream/yanshi -g -a codex -y
npx skills add Hackerismydream/yanshi -g -a claude-code -y
```

没有合适的 Node 时用 Python ≥ 3.10，默认只预览，`--apply` 才复制：

```bash
git clone https://github.com/Hackerismydream/yanshi && cd yanshi
python3 scripts/setup.py install --host both
python3 scripts/setup.py install --host both --apply
```

已有同名目录时脚本会拒绝。升级时加 `--update`：只替换 `skills.json` 里列出的目录，替换前先把原目录移到 `~/.yanshi-backup/<时间戳>/`；1.1 之前的旧快捷键目录只会列出，不会删除。见 [版本记录](CHANGELOG.md)。

## 让下次会话接回项目经验

读项目的入口会读目标项目的 `.yanshi/INDEX.md`，只用匹配情境的 `active` 条目；没有索引就继续，不创建文件。项目启动、测试、验收和真实坑记录在项目里，不塞进通用 Skill。

要让新会话也自动接回索引，在愿意启用的项目里配置一次（在克隆目录中运行）：

```bash
python3 scripts/setup.py project --project <你的项目根目录>
python3 scripts/setup.py project --project <你的项目根目录> --apply
```

脚本会创建空索引，向 Codex 实际生效的根入口文件（已有非空 `AGENTS.override.md` 时用它）和 `CLAUDE.md` 追加受控块，并把 `.yanshi/HANDOFF.md`、`.yanshi/evidence/` 加进项目 `.gitignore`。已有正文保留，重复执行不会重复追加。

retro 只有收到“记到项目 / 下次复用”等要求才保存。`candidate` 不生效；有真实原话、证据、适用范围及验证结果才标 `active`；失效记录标 `retired`。见 [项目沉淀](docs/project-memory.md)。

## 证据

验收时预期来自业务契约。成功提示不证明落库，要独立回读；UI 要实际操作；修复和重试保留原失败。

```bash
python3 scripts/check.py --self-test
```

检查覆盖范围见 [verification.md](verification.md)。[实践卡](docs/author-practices.md) 按“什么时候用 / 作者原话 / 为什么 / 真实例子”收录，其中“真实例子”大多仍空着。

## 命名与来源

偃师是《列子·汤问》里造出能歌善舞的机关人的工匠，取“指挥 Agent 干活”之意。

[设计说明](design-notes.md) · [宿主文档依据](docs/hosts.md) · [参与贡献](CONTRIBUTING.md) · [MIT](LICENSE)
