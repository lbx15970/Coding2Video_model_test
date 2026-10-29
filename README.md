# Coding2Video Model Test

客户给 coding-to-video 场景（自然语言 / 参考素材 → 模型写代码 → 渲染出视频），我们横向对比不同模型产出的视频质量、代码可复现性与稳定性。

被测模型两位主角：

| 模型 | 接入方式 | Endpoint | 配置 |
|---|---|---|---|
| Claude Opus 5.5 | 本 IDE 内置能力（人工/半自动驱动） | 无（IDE 会话） | [config.yaml](file:///Users/bytedance/PycharmProjects/Coding2Video_model_test/models/claude-opus-5.5/config.yaml) |
| Doubao-Seed-Evolving | 火山方舟 Ark API | `ep-20260812154547-t8rmk`（cn-beijing） | [config.yaml](file:///Users/bytedance/PycharmProjects/Coding2Video_model_test/models/seed-evolving/config.yaml) |

## 3 步开始

```bash
# 1) 建一次任务（自动生成带时间戳的目录 + 写台账）
python3 scripts/new_run.py --model seed-evolving --case case-001 --note "首测：KPI 柱状图动画"

# 2) 调模型（产物落在 outputs/<run_id>/）
python3 scripts/ark_client.py --run 20261029-141500_seed-evolving_case-001 \
    --prompt-file cases/case-001/prompt.md

# 3) 收尾：补全 run_meta / 结论，并校验目录与 README 同步
python3 scripts/check_tree.py
```

Claude Opus 5.5 不走脚本：在本 IDE 里把 `cases/<case-id>/prompt.md` 发给 Agent，产出代码和视频后，同样放进对应 `outputs/<run_id>/` 并登记台账。

## 铁律（每次任务前先读）

1. 先读本 README 的「目录结构」「任务执行流程」，再读 [RUNS.md](file:///Users/bytedance/PycharmProjects/Coding2Video_model_test/runs/RUNS.md) 最近 10 行。
2. 禁止手搓目录名，一律 `scripts/new_run.py` 生成 `YYYYMMDD-HHMMSS_<model>_<case>`。
3. 所有产物文件名以 run_id 开头：`<run_id>_v1.mp4`。
4. 增删目录后必须同步本 README 并跑 `scripts/check_tree.py`。
5. 密钥只放 `models/*/.env`（已 gitignore），不写进 YAML / 脚本 / commit。

## 目录结构

<!-- TREE:START -->
```
Coding2Video_model_test/
├── README.md                    # 本文件：项目说明 + 目录地图 + 执行规则
├── .gitignore                   # 屏蔽密钥、缓存、大媒体文件
├── .trae/
│   ├── rules/                   # 项目强制规则（Agent 每次任务自动加载）
│   └── skills/                  # IDE 侧 skill 挂载点
├── models/                      # 被测模型登记
│   ├── registry.yaml            # 模型总表：endpoint/region/版本/接入方式
│   ├── claude-opus-5.5/         # IDE 内置模型：参数与记录规则
│   └── seed-evolving/           # 方舟 API：endpoint、调用参数、.env 密钥
├── assets/                      # 公共素材（跨用例复用）
│   ├── manifest.md              # 素材来源/授权台账
│   ├── shared/                  # 通用截图、logo、字体
│   ├── targets/                 # 优秀目标视频（人工挑选的对标作品）
│   └── refs/                    # 参考输入
│       ├── videos/
│       ├── audio/
│       └── images/
├── cases/                       # 测试用例
│   ├── _template/               # 用例模板（case.yaml + prompt.md + 输入）
│   │   ├── case.yaml
│   │   ├── prompt.md
│   │   ├── inputs/              # 该用例专属参考素材
│   │   │   ├── videos/
│   │   │   ├── audio/
│   │   │   └── images/
│   │   └── targets/             # 该用例专属目标视频
│   └── <case-id>/               # 复制模板后填写
├── skills/                      # 互联网引入的 skill
│   ├── README.md                # 引入与登记规则（含安全底线）
│   ├── registry.yaml            # skill 总表：来源/版本/license/风险
│   └── <skill_name>/            # skill 代码与说明
├── scripts/
│   ├── new_run.py               # 建 run 目录 + 追加台账
│   ├── ark_client.py            # 方舟 Chat Completions 客户端，产物写 run 目录
│   └── check_tree.py            # README 目录树 vs 实际目录一致性校验
├── runs/
│   └── RUNS.md                  # 任务台账：时间/模型/用例/输入/输出/结论
├── outputs/                     # 所有生成物，按 run 隔离
│   └── <run_id>/                # 例 20261029-141500_seed-evolving_case-001
│       ├── videos/              # 最终视频
│       ├── code/                # 模型生成的代码
│       ├── frames/              # 抽帧（评调用）
│       ├── logs/                # request/response/content/error
│       └── run_meta.json        # 参数、版本号、耗时、结论
└── evals/                       # 评测
    ├── README.md                # 打分维度与门槛
    └── reports/                 # 每次 run 的评测报告
```
<!-- TREE:END -->

## 各目录职责

| 目录 | 放什么 | 不放什么 |
|---|---|---|
| `models/` | 模型接入信息、调用参数、版本号 | 视频产物、prompt |
| `assets/` | 跨用例复用的目标视频与参考素材 | 单次任务产物 |
| `cases/` | 用例定义（目标、输入、约束、prompt） | 生成结果 |
| `skills/` | 外部引入的 skill 源码与登记 | 密钥 |
| `scripts/` | 可复用脚本 | 一次性临时脚本（用完删） |
| `runs/RUNS.md` | 任务台账（唯一事实来源） | 大段分析正文（写进 evals/reports） |
| `outputs/<run_id>/` | 该次任务的全部产物 | 跨任务复用素材 |
| `evals/reports/` | 评测报告 | 视频文件 |

## 命名与时间戳规范

- `run_id`：`YYYYMMDD-HHMMSS_<model>_<case>`（Asia/Shanghai）
- 视频：`<run_id>_v<N>.mp4`，例如 `20261029-141500_seed-evolving_case-001_v1.mp4`
- 任务目录与台账行一一对应，台账是唯一索引；找不到产物先查 RUNS.md
- 同一次任务多次重跑：新建 run_id，不要覆盖旧目录

## 单次任务流程（SOP）

1. 读 README + RUNS.md → 确认模型、用例、是否已有同类结论
2. 有客户新场景：`cp -r cases/_template cases/<case-id>`，填 `case.yaml` / `prompt.md`，素材进 `inputs/`
3. 新模型：在 `models/registry.yaml` 加一条 + 建 `models/<key>/config.yaml` + 更新 README 模型表
4. `python3 scripts/new_run.py ...` 建 run，记下 run_id
5. 跑模型（脚本或 IDE），产物进 `outputs/<run_id>/`
6. 抽帧评调 → 写 `evals/reports/<run_id>.md` → 回填 `run_meta.json` 和 RUNS.md 结论
7. `python3 scripts/check_tree.py` 通过后收工

## 同步机制

README 的目录树被 `<!-- TREE:START -->` / `<!-- TREE:END -->` 包裹，[check_tree.py](file:///Users/bytedance/PycharmProjects/Coding2Video_model_test/scripts/check_tree.py) 会解析它并与磁盘实际目录逐条比对：

- 磁盘有、README 没有 → 报「未写入 README」并给出待补行
- README 有、磁盘没有 → 报「幽灵目录」
- `outputs/<run_id>/` 属动态目录，不参与校验；`<占位符>` 自动跳过

把它挂在提交前或每次任务收尾跑，README 就不会和实际目录漂移。

## 数据与密钥

- `ark-...` API key 只存在 `models/seed-evolving/.env`，已加入 `.gitignore`，**不会**被推到 GitHub；仓库里只留 `.env.example`
- 客户素材加 `cust_` 前缀，视为敏感数据；会外发到第三方的 skill 必须在 `skills/registry.yaml` 的 `risk` 字段标明
- 视频等大文件默认不入库（`.gitignore` 已屏蔽），确需入库再改用 Git LFS 并逐条放开
