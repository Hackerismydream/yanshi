---
name: yanshi-ask
description: "五个随时插入的思维小命令：first 重想问题 / challenge 找反例 / trim 做减法 / ablate 拆收益 / boundary 看边界。Manual thinking shortcuts: first, challenge, trim, ablate, boundary."
disable-model-invocation: true
---

# 思维小命令

用法：`$yanshi-ask <动作> <对象>`（Codex）或 `/yanshi-ask <动作> <对象>`（Claude Code）。只做用户点名的那一个动作，完成后回到原任务。未给动作时列出下面五个让用户选。

## first · 重想问题

> 不要基于 <既定方案> 继续设计。从第一性原理分析 <问题为什么发生>，以及最小必要的解决方案。

把尖括号换成当前问题。未确认的原因写成假设。

## challenge · 找反例

> 对这个方案做一次对抗性审查，优先寻找能推翻核心假设的反例。

给出反例与它推翻的假设；没验证过的反例不说成已发生的故障。

## trim · 做减法

> 用奥卡姆剃刀重新审查这个设计，在满足需求的前提下，删除所有非必要机制。

列出建议删除或简化的部分，以及删完仍需满足的需求。这是建议，动代码要用户确认。

## ablate · 拆收益

> 给这三个优化设计消融实验，判断真正的收益来自哪里。

按用户实际给出的优化数量设计。没跑过就不写收益数字。

## boundary · 看边界

> 按高内聚、低耦合原则审查 <目标模块> 的职责边界，不要为了拆而拆。

把目标模块换成本次对象，输出边界判断。
