# Coding2Video Model Test

给一个 coding-to-video 场景（一段 prompt + 可选参考素材），让模型写代码、渲染出视频，横向对比不同模型的产出。当前主测两个模型：

| 模型 | 接入方式 | Endpoint | 默认参数 |
|---|---|---|---|
| Claude Opus 5.5 | 本 IDE 内置能力（人工驱动） | 无 | temperature 0.7 / max_tokens 8192 |
| Doubao-Seed-Evolving | 火山方舟 Ark API | `ep-20260812154547-t8rmk`（cn-beijing） | temperature 0.7 / top_p 0.95 |

模型信息全部在 [models.yaml](file:///Users/bytedance/PycharmProjects/Coding2Video_model_test/models/models.yaml)，密钥在 `models/.env`（不入库）。

## 3 步开跑

```bash
# 1) 建任务：生成带时间戳的 outputs/<run_id>/，并自动在 runs/RUNS.md 记一行
python3 scripts/new_run.py --model seed-evolving --case case-001 --note "首测：KPI 柱状图动画"

# 2) 调模型：结果（含抽出的代码）落到该 run 目录
python3 scripts/ark_client.py --run 20261029-141500_seed-evolving_case-001 \
    --prompt-file cases/case-001/prompt.md

# 3) 收尾：把视频丢进 outputs/<run_id>/videos/，回填结论，然后校验 README 目录树没漂
python3 scripts/check_tree.py
```

Claude Opus 5.5 没有脚本：在本 IDE 里把 `cases/<case-id>/prompt.md` 交给 Agent，产物同样放 `outputs/<run_id>/`。

## 目录结构

<!-- TREE:START -->
```
Coding2Video_model_test/
├── README.md                    # 项目说明 + 目录地图 + 规则
├── .gitignore                   # 屏蔽密钥 / 缓存 / 大媒体文件
├── .trae/
│   └── rules/                   # 项目规则，Agent 每次任务自动加载
├── models/
│   ├── models.yaml              # 模型总表：endpoint、版本号、默认参数
│   ├── .env                     # API key（gitignored）
│   └── .env.example             # 密钥模板
├── cases/                       # 测试用例
│   ├── _template/               # 复制成 cases/<case-id>/ 后填写
│   │   ├── case.yaml            # 目标、输入、输出约束
│   │   ├── prompt.md            # 喂给模型的 prompt
│   │   ├── inputs/              # 该用例的参考 图/音/视频
│   │   └── targets/             # 该用例的目标视频（对标作品）
│   └── <case-id>/
├── assets/                      # 跨用例复用的公共素材
│   ├── targets/                 # 优秀目标视频
│   └── refs/                    # 参考输入素材
├── outputs/                     # 所有产物，按 run 隔离
│   └── <run_id>/                # 例 20261029-141500_seed-evolving_case-001
│       ├── videos/              # 最终视频
│       ├── code/                # 模型生成的代码
│       ├── logs/                # 请求/响应/推理过程
│       └── run_meta.json        # 实际参数、版本号、token、结论
├── runs/
│   └── RUNS.md                  # 任务台账：时间/模型/用例/输出/结论
├── scripts/
│   ├── new_run.py               # 建 run 目录 + 追加台账
│   ├── ark_client.py            # 方舟 Chat Completions 客户端
│   └── check_tree.py            # README 目录树 vs 实际目录校验
└── skills/
    └── registry.yaml            # 引入的互联网 skill 登记（来源/版本/license）
```
<!-- TREE:END -->

## 各目录一句话

| 目录 | 放什么 |
|---|---|
| `models/` | 模型接入信息与默认参数，一个 YAML 搞定 |
| `cases/` | 用例定义：prompt、参考素材、目标视频、输出约束 |
| `assets/` | 跨用例复用的目标视频与参考素材 |
| `outputs/<run_id>/` | 单次任务的全部产物，绝不跨任务混用 |
| `runs/RUNS.md` | 台账，唯一索引；找不到产物先查这里 |
| `scripts/` | 三个脚本：建 run / 调模型 / 校验目录 |
| `skills/` | 外部 skill 登记 |

## 命名规范

- `run_id` = `YYYYMMDD-HHMMSS_<model>_<case>`（Asia/Shanghai）
- 视频文件名以 run_id 开头：`<run_id>_v1.mp4`
- 同一次任务重跑就新建 run_id，不覆盖旧目录
- 客户素材加 `cust_` 前缀，视为敏感数据

## 每次任务的规则

1. 先读本 README「目录结构」+ [RUNS.md](file:///Users/bytedance/PycharmProjects/Coding2Video_model_test/runs/RUNS.md) 末尾几行，别重复踩坑。
2. 目录只用 `new_run.py` 生成，别手搓时间戳。
3. 新增/删除目录后更新本 README 目录树，跑 `python3 scripts/check_tree.py` 直到通过。
4. 新模型加到 `models.yaml`，新用例复制 `cases/_template`，新 skill 记到 `skills/registry.yaml`。
5. 密钥只放 `models/.env`。

## 怎么评

- 硬门槛：能播、时长/分辨率对、信息点无错字、无水印。
- 打分：内容准确性、视觉质量、节奏、参考还原度、代码可复现性，1-5 分。
- 结论写一行进 RUNS.md：`pass 4.2/5 | 优于 baseline 12% | 问题：结尾空镜过长`。

## 备注

- API key 只在 `models/.env`（已 gitignore），仓库里只有 `.env.example`。
- 视频/图片等大文件默认不入库；要入库请换 Git LFS。
