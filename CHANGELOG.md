# 变更记录

## v3：从十一层入口收敛为四个 Skill

删除通用转发层，集中于方案反例、真实业务取证与交叉审查。入口根据当前证据缺口选路，不再组织十个子步骤。

| v2 入口 | v3 去向 |
|---|---|
| yanshi | 保留，重写为缺口选路 |
| yanshi-design | 合并到新名称 yanshi-challenge |
| yanshi-review | 保留，聚焦交接、业务反例与修复复验 |
| yanshi-e2e | 保留，重写操作和取证规则 |
| yanshi-align、yanshi-split、yanshi-implement、yanshi-self-test | 删除；由宿主和项目原有能力完成 |
| yanshi-accept、yanshi-handoff | 合并到审查交接与 E2E 结果记录 |
| yanshi-retro | 删除独立入口；E2E 的 SOP 模板承接稳定路径沉淀 |

保留五个思维快捷键，补充每个方法的输入、具体反例与可检查输出。E2E 保留契约预期、独立回读、UI 边界与 P/F/B/U，另列成功耗时，防止快速失败造成速度优势的错觉。

运行时删除出处和补充设计标记，修复残句、重复标点与不存在的外部路径。仅入口和 E2E 开启隐式触发。全部调用改为读取真实存在的文件，不要求专有 Skill 工具。

同步中英文 README、llms.txt、安装名称与 Node 要求。MIT 和 Logo 路径保留；视觉文档缩为资产维护说明，不再混入旧工作流。增加包检查与故障注入回归，验证范围单独记录，不声称已有真实业务收益。

## 升级操作

备份旧安装，清理八个已删除名称：yanshi-align、yanshi-design、yanshi-split、yanshi-implement、yanshi-self-test、yanshi-accept、yanshi-handoff、yanshi-retro。

新版本的 `skills/` 是完整替换目录。不能只覆盖文件，否则旧 Skill 和旧参考文件仍会被发现。保留其他无关 Skill、原有图片、许可证和用户自有业务记录；本包不执行删除操作。

## v2

曾将单一工作流拆为总控与十个子 Skill，增加 E2E 目标、证据和方案对比模板。v3 保留这些模板的有效规则，移除转发与重复编排。
