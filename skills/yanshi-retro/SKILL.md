---
name: yanshi-retro
description: "复盘一下、把这次踩的坑记到项目里、下次别再犯 / Capture what went wrong and save the lesson in this project. 仅在用户明确要求回顾或沉淀时使用；不因编码结束自动写规则，口头总结不默认授权持久化。"
---

# 只记实际发生的事

读 [project-context.md](project-context.md)，以 `[偃师·记下来]` 开头说明本次是口头复盘还是已获准写入项目。

从本次实际对话、操作、失败和修复证据中，找出值得复用的做法。沿用 [practice-template.md](practice-template.md) 的四项：什么时候用 / 作者原话 / 为什么（踩过的坑） / 真实例子。没有原话或真实例子就保留空位，不把自己的建议改写成作者经验。

只要求“复盘”时直接输出；用户明确要求“记到项目 / 下次复用”后，读取 [storage.md](storage.md)，将本项目经验写入 `.yanshi/practices/` 并更新 `.yanshi/INDEX.md`。未验证的建议保存为 `candidate`，不能自动生效；具备原话、可核对的真实证据、适用范围且已验证的记录才写 `active`。

一个流程重复超过三次可以考虑做成 Skill，不是次数到了就强制生成。稳定操作可沉淀为 SOP；需要 E2E SOP 时用 [sop-template.md](sop-template.md)。无复用价值就不造文件。

复查旧规则是否仍有收益；过时条目保留历史并标 `retired`，不把一次局部修复扩成全局禁止。只更新用户授权的项目，不改安装的通用 Skill，不自动改宿主入口文件。返回实际写入路径、状态和下一次会读取什么。
