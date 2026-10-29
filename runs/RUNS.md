# 运行台账（唯一事实来源）

> 规则：每次任务由 `scripts/new_run.py` 自动追加一行；手工补「结论」时不要改已有行的时间与 run_id。
> 时间格式统一 `YYYY-MM-DD HH:MM:SS`（Asia/Shanghai）；run_id 格式 `YYYYMMDD-HHMMSS_<model>_<case>`。
> 场景/素材/环境准备不创建模型run，run_id和模型填`-`，状态记`prepared`；准备记录不是模型测试结果。

| 时间 | run_id | 模型 | 用例 | 关键输入 | 输出目录 | 状态 | 结论 |
|---|---|---|---|---|---|---|---|
| 2026-10-29 12:21:00 | 20261029-122100_init_project | - | 项目初始化 | 无 | 仓库根目录 | done | 建立目录骨架、模型登记、任务台账与同步校验脚本 |
| 2026-10-29 13:57:51 | 20261029-135751_seed-evolving_smoke-000 | seed-evolving | smoke-000 | - | outputs/20261029-135751_seed-evolving_smoke-000/ | done | 连通性 OK，实际版本 doubao-seed-evolving-latest-version；2401 tokens（其中 reasoning 1551），成功抽出 6 段代码。视频未渲染，仅验证链路 |
| 2026-10-29 14:18:29 | 20261029-141829_refactor_simplify | - | 结构精简 | - | 仓库根目录 | done | 目录 26→14：删除 evals/、.trae/skills、assets/shared、refs 三层分组、每模型目录、frames/；模型合并为 models.yaml，密钥收口到 models/.env；脚本同步改造 |
| 2026-10-29 18:17:38 | - | - | K1–K3、P1–P3、T1–T2、L1–L2场景准备 | 飞书场景文档；K3人工字幕样本 | cases/；assets/refs/；skills/registry.yaml；README.md | prepared | 已建10个用例的prompt/准备清单/确认点/验收；本机固定版本dashi和Remotion源码静态校验通过；P2完整规格、P1/P3未读细项、部分素材及T1技能原始来源待补；未调用模型、未运行生成或渲染、未新建模型run |
