# 项目规则

1. 任务前读 `README.md`（测试场景 + 目录结构 + 3 步开跑）和 `runs/RUNS.md` 末尾几行；测试操作者另读对应 `case.yaml` 检查准备状态。
2. 建 run 一律 `python3 scripts/new_run.py --model <key> --case <case-id>`，禁止手搓时间戳。
3. 产物进 `outputs/<run_id>/`，文件名以 run_id 开头：`<run_id>_v1.mp4`。
4. 增删目录后同步 README 目录树，并跑 `python3 scripts/check_tree.py` 直到通过。
5. 新模型 → `models/models.yaml`；新用例 → 复制 `cases/_template`；新 skill → `skills/registry.yaml`。
6. 密钥只放 `models/.env`（已 gitignore），不得写进 YAML / 脚本 / README / commit。
7. 收尾补全 `run_meta.json` 和 RUNS.md 的结论。
8. 仅做场景/素材/环境准备时不建模型run、不调用模型、不启动渲染或技能示例；在RUNS.md记录准备事项即可。
9. 被测模型只接收prompt和指定输入，不给K3标准答案或L2隐藏验收说明。缺少素材、原规格或工具先明确报告；各case按各自交互确认点执行。
10. 新用例只保留case.yaml和prompt.md，素材统一放assets/refs或assets/targets，以case-id作文件名前缀。互联网skill的本机入口与固定commit登记在skills/registry.yaml。
