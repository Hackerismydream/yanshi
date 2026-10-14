---
name: yanshi-build
description: "就按这个改、写完顺手测一下 / Build this and self-test it. 手动入口：需求已明确、要动手实现并自测时用。"
disable-model-invocation: true
---

# 动手，写完顺手测

读 [project-context.md](project-context.md)，用一句话说明当前改动与对应检查。

按已明确的需求做小范围变更。简单的直接实现；复杂任务只推进当前增量，独立部分才交给其他 Agent 在各自 worktree 中做，主 Agent 集成。

写完先跑相关自测：类型检查、测试和业务断言能发现的问题，交付前处理掉。检查命令从项目文档、manifest、脚本或 CI 里找；没条件执行就列明没测到什么。

发现过度设计就清掉非必要机制。修复已知问题后重新验证；遇到原因不明的失败，保留失败信息转入排障，而不是继续堆改动。

交付改动、实际检查结果和仍需在真实环境验证的业务目标。测试绿灯不等于需求理解正确，也不等于 E2E 通过。
