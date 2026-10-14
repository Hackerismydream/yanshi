<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/yanshi-logo-transparent-128.png">
    <img src="assets/logo/yanshi-logo-transparent-ink-128.png" alt="yanshi 偃师" width="120">
  </picture>
</p>

# yanshi 偃师 · v1.0

[English](README.md) · 中文

**我每天用 AI 开发的习惯。简单的直接做，复杂的按需加步骤，结论都有证据。**

这是作者自用验证版：实践来自已提供的文章、E2E 帖与本人纠正记录；没有会话证据的案例留空。入口、文件约定和宿主适配是本版设计，不冒充已经用了很久的经验。先日常使用，再决定哪些值得公开推荐。

## 一天里自然用起来

| 当前时刻 | 入口 | 直接这样说 |
|---|---|---|
| 不知道下一步 | [yanshi](skills/yanshi/SKILL.md) | 用偃师帮我推进，看看下一步做什么 |
| 接到需求，开工前 | [yanshi-think](skills/yanshi-think/SKILL.md) | 帮我想想怎么做，先别急着写 |
| 目标明确，写代码 | [yanshi-build](skills/yanshi-build/SKILL.md) | 就按这个改，写完顺手测一下 |
| 卡住了，出 bug | [yanshi-debug](skills/yanshi-debug/SKILL.md) | 这个 bug 怎么回事，先帮我查一下 |
| 提交、合并前 | [yanshi-check](skills/yanshi-check/SKILL.md) | 提交前帮我看一眼，确认真的能用 |
| 上下文满了，换会话 | [yanshi-handoff](skills/yanshi-handoff/SKILL.md) | 上下文快满了，整理一下给下个会话 |
| 需求做完，记录经验 | [yanshi-retro](skills/yanshi-retro/SKILL.md) | 复盘一下，把这次踩的坑记到项目里 |

总控只选当前一步，不把这些入口串成流水线。明确的小修改直接写和测，不要求产生 Spec、任务表和复盘文件；只读检查不获得修复权限。

## 五个随时插入的小命令

| 命令 | 动作 | 日常说法 |
|---|---|---|
| `yanshi-first` | 重想问题 | 别沿着这个方案想了，从头分析原因 |
| `yanshi-challenge` | 找反例 | 别帮它找理由，找个能推翻它的反例 |
| `yanshi-trim` | 做减法 | 是不是太复杂了，把不必要的删掉 |
| `yanshi-ablate` | 拆收益 | 这几个优化，到底哪个有用 |
| `yanshi-boundary` | 看边界 | 看看职责有没有混在一起，别为了拆而拆 |

Codex 用 `$yanshi-challenge`，Claude Code 用 `/yanshi-challenge`；其他名字同理。这些快捷键保留作者短 Prompt 的核心动作，默认主动调用，不自动组合成五轮分析。中英文触发句和边界见 [使用表](docs/usage.md)。

## 安装到 Codex 和 Claude Code

skills CLI 需要 **Node ≥ 22.20**。先在本地试用本交付包，从解压目录运行：

```bash
npx skills add . --skill '*' -g -a codex -a claude-code
```

发布到仓库后才用远端命令：

```bash
npx skills add Hackerismydream/yanshi --skill '*' -g -a codex -a claude-code
```

只装某个入口，将 `'*'` 换成对应名字，例如 `yanshi-debug`。专业入口各自包含所需资料；总控要路由六个时刻，应安装完整套件。远端命令不会安装尚未发布的本地 ZIP。

没有合适的 Node 时可用本包脚本，默认只预览；`--apply` 才复制：

```bash
python3 scripts/setup.py install --host both
python3 scripts/setup.py install --host both --apply
```

脚本需要 Python ≥ 3.10。所有目标预检后才复制；发现已有目录或悬空符号链接就退出，不覆盖任何已有 Skill。升级请先按 [迁移说明](CHANGELOG.md) 处理旧目录，不运行全局清空命令。每个 Skill 的 `agents/openai.yaml` 与 Claude Code 的 frontmatter 控制分别配置；安装文件存在不等于宿主执行通过。

## 让下次会话接回项目经验

每个 Skill 会读目标项目的 `.yanshi/INDEX.md`，再读匹配情境的 `active` 条目；没有索引就继续，不创建空文件。项目启动、测试、验收和真实坑记录在项目里，不塞进通用 Skill。

要在新会话中也自动接回索引，只在愿意启用的项目做一次配置。以下 `.` 指目标项目根目录，脚本路径换成你解压本包的实际位置：

```bash
python3 /实际解压路径/yanshi-v1.0/scripts/setup.py project --project .
python3 /实际解压路径/yanshi-v1.0/scripts/setup.py project --project . --apply
```

脚本会预览并追加受控块到 Codex 实际适用的根入口文件和 `CLAUDE.md`，创建不含业务规则的索引；保留已有正文，不写全局配置。已有非空 `AGENTS.override.md` 时使用它，避免写进被忽略的 `AGENTS.md`。配置是一次性选择，不是所有任务的前置步骤。

retro 只有收到“记到项目 / 下次复用”等写入要求才保存。`candidate` 不自动生效；有真实原话、证据、适用范围及验证结果才标 `active`；失效记录标 `retired`。自动读取是宿主启动指令加 Skill 的文件读取，不是后台服务，也不保证任意会话都正确遵从。约定与冲突处理见 [项目沉淀](docs/project-memory.md)。

## 看得见，但不拿标识冒充证据

`[偃师·动手] 直接改当前增量并跑相关自测 · 项目经验：1 条`

这是输出形式示例，不是一次已执行记录。每次采用入口的首条进展只显示一行；经验数量必须来自实际读取。完成与否仍看真实结果和证据。

验收时预期来自业务契约。成功提示不证明落库；UI 要实际操作；修复和重试保留原失败。不要求先写一套传统测试用例，也不普遍禁止 AI 写测试。

## 检查与自用记录

```bash
python3 scripts/check.py --self-test
```

包检查、脚本测试和宿主实测分别记录在 [verification.md](verification.md)。当前没有完成 Codex / Claude Code 的真实模型会话验收，不能写成“两个宿主已跑通”。可直接交给本地 Codex 的任务见 [docs/codex-task.md](docs/codex-task.md)。

每条作者实践按“什么时候用 / 作者原话 / 为什么（踩过的坑） / 真实例子”收录在 [实践卡](docs/author-practices.md)；缺失材料见 [收集清单](docs/author-evidence-request.md)。原文举例不冒充真实项目事故或性能实验。

## 命名、Logo 与来源

偃师是《列子·汤问》里造出能歌善舞的机关人的工匠，取“指挥 Agent 干活”之意。README 沿用原有深浅主题 Logo；Skill 单独安装不带仓库资产，因此不填跨目录 icon 路径。

[原文](https://x.com/huangtongxueh/status/2108577165306687938) · [E2E 帖](https://x.com/huangtongxueh/status/2109687887264681986) · [来源与设计边界](design-notes.md) · [宿主文档依据](docs/hosts.md)

[MIT](LICENSE)。`1.0.0` 是新的产品版本，不是对“日常验证完成”的承诺。
