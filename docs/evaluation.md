# 评测计划：装与不装 yanshi

状态：**计划，尚未执行，没有结果。** 下文所有表格都是口径与待办，不是成绩。骨架在 [evals/](../evals/README.md)。

## 要回答的问题

1. 用日常说法提需求时，宿主能不能选对 yanshi 的入口。
2. 按业务契约判定，装 yanshi 后任务成功率有没有变化。
3. 结论有没有附可核对的证据；“说做完了但其实没做完”的比例有没有下降。
4. 代价：工具调用、token、耗时各变化多少。

只在本任务集、本次宿主版本下回答这些问题。样本小，不做显著性结论，只报原始计数。

## 设计

| 项 | 约定 |
|---|---|
| 宿主 | Codex（`codex exec`）、Claude Code（`claude -p`），用户已有的正常登录；不写死模型，运行时记录宿主版本 |
| 组 | **with**：skills 装进该 trial 的 checkout（`setup.py install --home <checkout>`）；**without**：不装 |
| 隔离 | 全局 `~/.agents/skills/`、`~/.claude/skills/` 里有 yanshi 时不跑；每个 trial 重新 checkout，互不继承状态 |
| 公平 | 两组用同一条 CLI 命令、同一 checkout、同一句提示。手动入口（`yanshi-build`）只在 with 组加 `$` / `/` 前缀，这部分结果单独报告，因为点名本身就是差异 |
| 重复 | 每个 任务 × 宿主 × 组 跑 3 次；每个组合 N = 任务数 × 3，运行前固定 |
| 顺序 | runner 对每个任务交替跑两组，减少时段与缓存带来的系统偏差；冷 / 热状态在 run.json 旁注明 |
| 权限 | 需要执行测试的任务只在一次性容器或虚拟机里放宽权限；两组用同一权限设置并记录 |
| 预算 | 运行前写下批准的费用上限；超预算未跑的 trial 记 U，不删 |

先在一个宿主、一个任务上跑 1 次冒烟，确认 with 组的 transcript 里能看到 yanshi 被发现（项目级 skills 目录是否被宿主读取要实测，不假设）。

## 任务集（14 个 + 选路探针）

选择已合并修复的公开仓库问题，用上游修复附带的测试作为业务契约。下列 PR 均已在上游核对过标题与对应 issue；它们也以 `owner__repo-PR号` 的形式出现在 SWE-bench 中时，`base_commit`、`test_patch`、`FAIL_TO_PASS` / `PASS_TO_PASS` 直接取数据集该行。数据集里查不到的，用 PR 合并前的父提交并自建隐藏测试补丁。**base_commit 一律在运行前从数据集或 git 历史取得，现在不填猜测值。**

| id | 时刻 | 上游 | 提示要点（日常说法，不泄露修法） | 契约 |
|---|---|---|---|---|
| T1 | think | [sympy#20590](https://github.com/sympy/sympy/pull/20590)（issue #20567） | Symbol 从 1.7 起有了 `__dict__`，帮我想想怎么做 | 评分表：定位到缺 `__slots__` 的 mixin；验收来自“Symbol 不应有 `__dict__`”；无代码改动 |
| T2 | think | [astropy#12907](https://github.com/astropy/astropy/pull/12907)（issue #12906） | 嵌套 CompoundModel 的 `separability_matrix` 结果不对，先别写，想想 | 评分表：指出右侧为复合模型时的处理问题；给出可独立验收的增量；无代码改动 |
| T3 | think | TODO：选一个需要取舍的功能请求 | — | — |
| B1 | build | [flask#4045](https://github.com/pallets/flask/pull/4045)（issue #4041） | Blueprint 名字不能含点，就按这个改，写完顺手测一下 | 隐藏测试 |
| B2 | build | [django#11133](https://github.com/django/django/pull/11133)（ticket #30294） | HttpResponse 要能接受 memoryview 内容 | 隐藏测试 |
| B3 | build | [pytest#5227](https://github.com/pytest-dev/pytest/pull/5227)（issue #5214） | 按 issue 改进默认日志格式 | 隐藏测试 |
| D1 | debug | [django#11099](https://github.com/django/django/pull/11099)（ticket #30257） | 用户名末尾带换行居然能注册，查一下并修 | 隐藏测试 |
| D2 | debug | [django#11179](https://github.com/django/django/pull/11179)（ticket #30330） | 快速删除后实例的主键还在，怎么回事 | 隐藏测试 |
| D3 | debug | [scikit-learn#13142](https://github.com/scikit-learn/scikit-learn/pull/13142)（issue #13070） | `n_init > 1` 时 `fit_predict` 和 `fit().predict` 结果不一致 | 隐藏测试 |
| D4 | debug | [requests#2317](https://github.com/psf/requests/pull/2317)（issue #2316） | 方法名传 bytes 时请求发出去变成了 `b'GET'` 一类的字符串 | 隐藏测试 |
| C1 | check | D1 的变异补丁：只改 ASCII 校验器，漏掉 Unicode 校验器 | 提交前帮我看一眼，确认真的能用，别改代码 | 结论应为“不能提交”；无代码改动 |
| C2 | check | D3 的上游修复原样作为待审改动 | 同上 | 结论应为“可以提交”（衡量误报）；无代码改动 |
| C3 | check | [requests#2148](https://github.com/psf/requests/pull/2148)（issue #2144）的变异补丁：TODO 构造 | 同上 | 结论应为“不能提交” |
| C4 | check | B1 的上游修复原样作为待审改动 | 同上 | 结论应为“可以提交” |

变异补丁由评测者构造并存档在 `evals/fixtures/`，要求：已有测试全部通过，至少一个 `FAIL_TO_PASS` 测试失败。这样“测试是绿的”不等于需求达成，正好对应 `yanshi-check` 要防的情况。

**选路探针**（只评选中的入口，不评任务成败）：在任一已 checkout 的仓库里，用 [docs/usage.md](usage.md) 五个自动入口的中英文说法各一句，再各加一句换了措辞的说法；另加反例——“把这个函数改一下”“下一步做什么”（`yanshi`、`yanshi-build` 不应被自动选中）、翻译一段文字（不应触发任何入口）、只说“复盘一下”（不应写项目文件）。

已知局限：这些问题都是公开的，可能出现在模型训练数据里。两组受到的影响相同，所以只比较组间差异，绝对通过率不和任何外部榜单比。

## 指标

| 指标 | 定义 | 怎么取 |
|---|---|---|
| 选路准确率 | with 组中 实际入口 = 预期入口 的 trial 数 / 有预期入口且已尝试的 trial 数；另列手动入口被自动触发次数、反例被触发次数 | transcript 里的 Skill 调用或对应 `SKILL.md` 读取；runner 自动抽取，评分人确认 |
| 任务成功（业务契约） | build / debug：`FAIL_TO_PASS` 全过且 `PASS_TO_PASS` 无回退；think：评分表全部满足且 diff 为空；check：结论与预期一致且 diff 为空 | 隐藏测试在 Agent 结束后才应用并运行；评分表由人按条目判 |
| 证据在场 | 最终报告里每个“通过 / 已修复 / 可以提交”的说法，都能在 transcript 里找到实际执行的命令及其输出；未验证的部分有单独列出 | 评分人对照 `stdout.jsonl` 判 y / n |
| 代价 | 工具调用数、输入 / 输出 token、墙钟时间 | 宿主原始输出；拿不到的记“未知”，不按零计 |
| false pass 率 | Agent 声称完成或“可以提交”、但契约判定失败的 trial 数 / 契约判定失败的 trial 数 | `agent_claimed_pass` 与 `contract_passed` 两列 |
| 误报率（check） | 对 C2、C4 这类正确改动，结论为“不能提交”的比例 | 同上 |

## P / F / B / U 计数

沿用 [yanshi-check 的对比模板](../skills/yanshi-check/comparison-template.md)：

- **P**：契约判定通过。**F**：已尝试但契约失败，包括超时和交付了错误结论。**B**：环境、登录、权限或宿主故障导致无法完成。**U**：计划内但没跑（字段仍为 TODO、预算用尽）。
- 每个 宿主 × 组 的 N 在运行前固定，始终满足 `N = P + F + B + U`；失败的任务不删，补跑另报。
- 通过率报原始分数 `P/N`，同时列出 F、B、U。已尝试 trial 的平均耗时用 `P + F + B` 作分母并写出分母；另列成功 trial 的平均耗时。
- 修改被测代码、任务或契约后建立新批次，不覆盖旧记录。没有完整数据，不排名。

## 评分流程

1. 先跑客观部分：隐藏测试、diff 是否为空。runner 预填 `contract_passed`。
2. 再做人工部分：评分表、证据在场、Agent 是否声称完成。评分时尽量只看最终报告与 diff，去掉 `[偃师·…]` 标识，减少对组别的感知。
3. think 任务和证据在场两项，抽 20% 由第二位评分人独立判，分歧原样记录。
4. `python3 evals/run.py summarize evals/runs/<时间戳>` 出汇总表；有未评分行时拒绝汇总。

## 运行记录

布局见 [evals/README.md](../evals/README.md)。原始日志留在本地 `evals/runs/<时间戳>/`（已 gitignore）。发布结果时提交汇总表、`grades.csv`、`run.json` 与评分说明，并写明原始日志的存档位置；未跑完的批次标明“未完成”，不给结论。

## 跑一遍

```bash
python3 -m pip install pyyaml
# 1. 在 evals/tasks.yaml 里把模板复制为正式任务，填 base_commit 与契约
python3 evals/run.py run --dry-run
# 2. 冒烟：一个宿主、一个任务、一次
python3 evals/run.py run --hosts claude-code --only <id> --repeats 1 --keep-work
# 3. 全量
python3 evals/run.py run
# 4. 填 grades.csv 后汇总
python3 evals/run.py summarize evals/runs/<时间戳>
```

---

## 两周 dogfooding（作者）

A/B 评测回答“有没有用”，dogfooding 解决另一件事：把 [实践卡](author-practices.md) 里空着的“真实例子”用真实会话填上。两周结束只报告发生了什么，不把试用当成收益证据。

**第 0 天**

- 在日常机器上全局安装 yanshi；在 1–2 个真实工作项目里执行 `python3 scripts/setup.py project --project <项目根目录> --apply`。
- 在每个项目建 `.yanshi/evidence/dogfood.md`（`.yanshi/evidence/` 已被 setup 加入 `.gitignore`）。
- 跑 A/B 前记得把全局 yanshi 移开，否则 runner 会拒绝运行。

**每天**

- 先用日常说法，不点名 Skill，看宿主自己选什么；只有 `yanshi-build`、`yanshi`、`yanshi-ask` 需要点名。
- 每个用到的时刻在 `dogfood.md` 记一行：

  | 日期 | 项目 | 原话 | 期望入口 | 实际入口 | 结果 | 证据位置 | 摩擦 / 错选 |
  |---|---|---|---|---|---|---|---|

- 重点记这几类：选错入口；小改动被拖进重流程；check 说没问题但后来出错（false pass）；handoff 后新会话接错；`yanshi-ask` 某个动作改变了决定。

**每天收工（5 分钟）**

- 当天有失败或意外时，直接说“复盘一下，把这次踩的坑记到项目里”。`yanshi-retro` 会在 `.yanshi/practices/` 写一条 `candidate`，带上原话和证据位置；缺材料的项留空。

**每周末（第 7、14 天）**

- 逐条复查 `candidate`：原话、证据、适用范围都核对过且验证过的，改为 `active`；没用的标 `retired`。
- 挑出能对应到某张实践卡的记录，脱敏后写进 [author-practices.md](author-practices.md) 对应卡片的“真实例子”：日期、当时说的原话、发生了什么、怎么验证的（与 [CONTRIBUTING](../CONTRIBUTING.md#help-collect-real-examples) 的要求一致）。“作者原话”一栏仍只收逐字原文。
- 选路错误攒在一起看：要改 description 时，先保留错选轨迹，改完用上面的选路探针在两个宿主各重跑一遍。

**第 14 天交付**

- 每个入口被用到的次数、错选次数、retro 产生 / 转正 / 退休的条数、实践卡里仍空着的例子。
- 哪些发现要转成 A/B 任务集里的新任务（例如一次真实的 false pass）。
