---
name: yanshi-retro
description: "复盘一下、把这次踩的坑记到项目里、下次别再犯 / Capture what went wrong and save the lesson in this project. 用户明确要求复盘或沉淀经验时用。"
---

# 只记实际发生的事

读 [project-context.md](project-context.md)，说明本次是口头复盘还是已获准写入项目。

从本次实际对话、操作、失败和修复证据中找出值得复用的做法，按 [practice-template.md](practice-template.md) 的四项记录：什么时候用 / 作者原话 / 为什么（踩过的坑） / 真实例子。缺原话或真实例子就留空，不把自己的建议写成作者经验。

只要求“复盘”时直接输出；用户明确要求“记到项目 / 下次复用”后，读 [storage.md](storage.md)，写入 `.yanshi/practices/` 并更新 `.yanshi/INDEX.md`。未验证的记录存为 `candidate`；具备原话、可核对证据、适用范围且已验证才写 `active`。

一个流程重复超过三次，可以考虑做成 Skill；稳定操作可沉淀为 SOP，E2E SOP 用 [sop-template.md](sop-template.md)。

复查旧规则是否仍有收益；过时条目标 `retired` 并保留历史，一次局部修复不扩成全局禁止。只写用户授权的项目，安装的通用 Skill 和宿主入口文件保持原样。返回实际写入路径、状态和下次会读取什么。
