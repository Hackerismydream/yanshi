# evals

装与不装 yanshi 的 A/B 评测骨架。计划、任务清单与评分口径见 [docs/evaluation.md](../docs/evaluation.md)。**目前没有任何运行结果**；这里只有任务模板和 runner。

| 文件 | 作用 |
|---|---|
| [tasks.yaml](tasks.yaml) | 宿主命令与任务。现有条目都是 `template: true` 的模板，runner 默认跳过 |
| [run.py](run.py) | 按 任务 × 宿主 × 组 × 重复 逐个 trial 调 `claude -p` / `codex exec`，保存原始输出；`summarize` 按 P/F/B/U 计数 |
| `runs/` | 每次运行一个 `<时间戳>/` 目录，已加入 `.gitignore`，只在本地保留 |
| `fixtures/` | 隐藏测试补丁与 check 任务的变异补丁（按需创建，见 tasks.yaml 注释） |

## 运行

需要 Python ≥ 3.10、PyYAML、git，以及已登录的 Codex 和 / 或 Claude Code。

```bash
python3 -m pip install pyyaml
python3 evals/run.py run --dry-run --include-templates     # 只打印计划，不调用宿主
python3 evals/run.py run --hosts claude-code --only <任务 id> --repeats 1
python3 evals/run.py summarize evals/runs/<时间戳>
```

with 组把 skills 装进该 trial 的 checkout（项目级 `.agents/skills/`、`.claude/skills/`），without 组什么都不装。全局已装 yanshi 时 runner 拒绝运行，因为 without 组也会看到它；先移开，或加 `--allow-global-skills` 并在结果里写明污染。

## 每个 trial 留下什么

```
runs/<时间戳>/
  run.json            宿主版本、yanshi 提交、计划 trial 数
  grades.csv          每个 trial 一行；runner 预填可自动取得的列，P/F/B/U 由评分人填写
  <task>__<host>__<arm>__r<n>/
    meta.json         实际命令、起止时间、退出码、尽力解析的工具调用与 token
    stdout.jsonl      宿主原始输出
    stderr.txt
    diff.patch        Agent 的全部改动（不含预置补丁和 skills 目录）
    contract.txt      隐藏测试输出（任务配置了 contract.command 时）
```

`--keep-work` 保留每个 trial 的 checkout 以便检查。runner 不判定成败，只记录；`routed_skills_auto` 和 token 是从原始输出尽力解析的，评分时对照 `stdout.jsonl` 确认。
