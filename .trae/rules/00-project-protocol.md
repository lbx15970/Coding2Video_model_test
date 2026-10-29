# 任务前必读

1. 每次开始任何任务（包括只跑一条命令）前，先读根目录 `README.md` 的「目录结构」和「任务执行流程」两节。
2. 读 `runs/RUNS.md` 最近 10 行，确认上次 run 的模型、用例、输入、结论，避免重复踩坑。
3. 新任务一律用 `python3 scripts/new_run.py --model <模型key> --case <用例id>` 建目录，禁止手搓时间戳。
4. 所有产物落在 `outputs/<run_id>/`，文件名前缀必须是 `<run_id>`；不接受无时间戳的 mp4。
5. 新增/删除/改名任何目录后，必须同步更新 `README.md` 的目录树，并跑 `python3 scripts/check_tree.py` 直到通过。
6. 新模型、新用例、新引入的互联网 skill 都要登记：`models/registry.yaml`、`cases/`、`skills/registry.yaml`，并在 README 对应说明里出现。
7. 密钥只放 `models/<model>/.env`（已 gitignore），不得写进 YAML、脚本、README、commit message。
8. 交付/汇报前把 `run_meta.json` 补全（版本号、实际参数、耗时、结论）。
