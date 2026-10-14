# 版本记录

状态说明：这是作者自用版本，Codex / Claude Code 真实会话和业务效果尚未验证，实践卡的真实例子仍在收集。

## 1.1.0

- 五个思维快捷键 `yanshi-first`、`yanshi-challenge`、`yanshi-trim`、`yanshi-ablate`、`yanshi-boundary` 合并为一个手动 Skill `yanshi-ask`，用法 `$yanshi-ask first …` / `/yanshi-ask trim …`；作者原 Prompt 逐字保留。
- `yanshi` 总控和 `yanshi-build` 改为手动入口，普通编码请求不再被隐式匹配。
- `project-context.md` 缩为三行；`yanshi-ask` 不读项目上下文；首行标识改为可选。
- 各 SKILL.md 删去大部分防御性否定句；debug 的查库、日志、Trace 按场景选择。
- `setup.py install --update`：只替换 `skills.json` 中列出的目录，替换前备份到 `~/.yanshi-backup/<时间戳>/`。
- `setup.py project` 往目标项目 `.gitignore` 加 `.yanshi/HANDOFF.md` 与 `.yanshi/evidence/`；INDEX 统一使用 `skills/yanshi-retro/index-template.md`。
- `check.py` 只做结构校验。
- 删除构建过程文档、未被引用的图片和重复图片；新增 [CONTRIBUTING.md](CONTRIBUTING.md) 说明需要收集哪些真实例子。

### 从 1.0 升级

```bash
git clone https://github.com/Hackerismydream/yanshi && cd yanshi
python3 scripts/setup.py install --host both --update          # 预览
python3 scripts/setup.py install --host both --update --apply
```

脚本会列出仍留在安装目录的旧快捷键目录（标为 `OBSOLETE`），确认后手动删除即可。项目里的 `.yanshi/` 不受影响。

## 1.0.0

- 用六个日常时刻代替研发阶段：想清楚、动手、排障、验一下、交接、记下来；总控只选当前路径。
- 五个思维快捷键单独安装、手动调用。
- 通用实践与项目经验分开：retro 的记录存在目标项目；新会话可通过一次性宿主配置读回索引。
- 日常入口使用中英文口语触发句。

### 从 v3 迁移

| 旧名字 | 新去向 |
|---|---|
| yanshi | 保留名称，改为日常时刻路由 |
| yanshi-challenge | 1.0 收窄成一句对抗性审查；1.1 并入 `yanshi-ask challenge` |
| yanshi-e2e | 合入 yanshi-check 的真实业务验收资料 |
| yanshi-review | 合入 yanshi-check 的提交前审查 |

v2 曾同名的 handoff/retro 需整体替换。用 `setup.py install --update` 升级会先备份同名目录；只清理已确认的旧 yanshi 名称，保留项目 `.yanshi`、`CONTEXT.md` 和已有宿主指令。

## 实验稿 v3

四个入口，聚焦方案反例、E2E 取证和交叉审查。
