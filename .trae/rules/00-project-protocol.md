# 项目规则

1. 任务前读 `README.md`（目录结构 + 3 步开跑）和 `runs/RUNS.md` 末尾几行。
2. 建 run 一律 `python3 scripts/new_run.py --model <key> --case <case-id>`，禁止手搓时间戳。
3. 产物进 `outputs/<run_id>/`，文件名以 run_id 开头：`<run_id>_v1.mp4`。
4. 增删目录后同步 README 目录树，并跑 `python3 scripts/check_tree.py` 直到通过。
5. 新模型 → `models/models.yaml`；新用例 → 复制 `cases/_template`；新 skill → `skills/registry.yaml`。
6. 密钥只放 `models/.env`（已 gitignore），不得写进 YAML / 脚本 / README / commit。
7. 收尾补全 `run_meta.json` 和 RUNS.md 的结论。
