# 验证记录

版本 1.1.0。仓库共 57 个 git 跟踪文件（`git ls-files | wc -l`）：8 个 Skill、2 张 README Logo，其余为文本与脚本。

## 可复现的检查

```bash
python3 scripts/check.py --self-test
```

`check.py` 只做结构校验：

| 检查 | 内容 |
|---|---|
| 必需文件 | README、CHANGELOG、CONTRIBUTING、docs、scripts 等存在 |
| 目录与目录表 | `skills/` 下的目录与 `skills.json` 一一对应，版本与 `VERSION` 一致 |
| frontmatter 与 sidecar | 名称与目录一致、描述含中英文；`skills.json` 的 `implicit`、frontmatter 的 `disable-model-invocation`、`agents/openai.yaml` 的 `allow_implicit_invocation` 三处一致 |
| 链接 | Markdown 与 llms.txt 中的本地链接和图片都能解析；非总控 Skill 不链接自身目录以外的文件（保证单独安装可用） |
| 项目读取约定 | 各 `project-context.md` 副本字节相同 |
| 文档同步 | README、README_CN、llms.txt、docs/usage.md 都列出全部 Skill |
| 模型名 | 文本中没有写死的模型型号 |
| 引语 | `docs/author-practices.md` 包含 `docs/source-excerpts.json` 中的每段引语（两者互相比对，不代表与外部原文重新核对） |

`--self-test` 另跑 `scripts/test_setup.py`，在临时 HOME / 项目目录里测试安装、`--update` 备份与回滚、项目接入、`.gitignore` 追加和幂等性。最近一次输出见 [check-output.txt](verification/check-output.txt)。

## 尚未验证

Codex / Claude Code 真实会话中的发现、自然语言选路、手动入口、项目经验采用和跨会话读回都还没有执行；在线 `npx skills add` 安装与业务 E2E 也没有执行。状态见 [host-results.json](verification/host-results.json)，执行步骤见 [host-validation.md](docs/host-validation.md)。
