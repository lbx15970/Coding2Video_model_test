# Coding2Video Model Test

给一个 coding-to-video 场景（一段 prompt + 可选参考素材），让模型写代码、渲染出视频，横向对比不同模型的产出。当前主测两个模型：

| 模型 | 接入方式 | Endpoint | 默认参数 |
|---|---|---|---|
| Claude Opus 5.5 | 本 IDE 内置能力（人工驱动） | 无 | temperature 0.7 / max_tokens 8192 |
| Doubao-Seed-Evolving | 火山方舟 Ark API | `ep-20260812154547-t8rmk`（cn-beijing） | temperature 0.7 / top_p 0.95 |

模型信息全部在 [models.yaml](models/models.yaml)，密钥在 `models/.env`（不入库）。

## 3 步开跑

先在下表选用例，读它的 `case.yaml` 和 `prompt.md`，补齐 `preparation` 中的输入与待确认项。当前仅完成场景准备，未运行这些用例。

```bash
# 1) 建任务：生成带时间戳的 outputs/<run_id>/，并自动在 runs/RUNS.md 记一行
python3 scripts/new_run.py --model seed-evolving --case K1 --note "信息卡包装首测"

# 2) 在 Agent 测试环境中提交 cases/K1/prompt.md 和对应素材，按该 case 的确认点逐步执行
#    Claude 使用 IDE；Seed 使用带同等工具的 Agent 环境。记下上一条命令实际返回的 run_id。

# 3) 收尾：将产物归档到该 run，回填实际版本、参数、工具、输入、耗时与结论
python3 scripts/check_tree.py
```

`ark_client.py` 目前只提供单轮文本/图片调用，不带视频获取、ASR、浏览器、代码执行或多轮 Agent 循环。它可以验证模型接口，不能独立完成这些场景。正式横评时，两模型需要相同工具、输入、skill 版本和用户反馈；缺工具或链接不可访问单独记为环境问题。

## 测试场景

来源：[Coding to video - 场景示例](https://flova-team.feishu.cn/docx/Ls5Gdp6SworOVoxUQXvcQPMInYd)，2026-10-29 整理。每个用例只有 `case.yaml`（输入、步骤、验收、待补项）和 `prompt.md`（被测模型输入），素材统一放 `assets/`。

| 用例 | 测什么 | 规格 / 交付 | 开始前需补齐 |
|---|---|---|---|
| [K1](cases/K1/case.yaml) | 口播信息卡、六步确认、定向修改 | 1920×1080，保留原声，样片15–25秒 | 客户口播、信息卡目标视频、完整片长与fps |
| [K2](cases/K2/case.yaml) | dashi讲解动画、关键词同步 | 1920×1080、30fps，时长随口播，第1种立体卡通 | 15–60秒口播、逐字稿；精确对齐工具 |
| [K3](cases/K3/case.yaml) | 9项红色+6项黄色字幕质检 | 问题报告 → 确认后只修红色字幕 | 匹配口播/字幕、剪辑点与fps |
| [P1](cases/P1/case.yaml) | 12种UI连续形变、卡拍、无缝循环 | 14秒、1440×1440、约120BPM | 音乐、Geist、fps及原长prompt未读细项 |
| [P2](cases/P2/case.yaml) | 换品牌复刻、长规格遵循 | 12秒，逐帧规格对照 | **完整原prompt/约1万字规格**、参考片、品牌资料、画幅fps |
| [P3](cases/P3/case.yaml) | 真实网站截图、连续3D飞越 | 14.5秒、1440×1152、60fps、无配乐 | 原长prompt未读细项、字体；测试时验证网站访问 |
| [T1](cases/T1/case.yaml) | 六文件工作流、数据来源、只改一行 | 30秒、1080×1350 | 参考片、motion-design-skill确切来源、fps与业务数据核验 |
| [T2](cases/T2/case.yaml) | 七段中文模板、确定性渲染、代码配乐 | 30秒、1080×1920、30fps | 思源黑体、numpy/scipy；原文截断处先确认 |
| [L1](cases/L1/case.yaml) | 看视频学方法、提取原话与学习卡 | 学习卡和可用指令，**不出视频** | 测试时验证链接；人工学习报告尚未提供 |
| [L2](cases/L2/case.yaml) | 只给链接、拆规格后代码复刻 | 15秒、无声音、同步抽帧对照 | 测试时获取原片并确认画幅fps |

本批 `prompt.md` 是注明来源的整理版，不冒充逐字原文。P2 正文和完整规格尚未取得；P1/P3 已读场景与 direction，后续细项未完整读取。T2 的 `[画面截断]` 是原文已有标记，保留它，不补写成作者原话。

教学原帖用于理解方法，不能把 K1/K2 的教学视频当客户口播，或把链接存在当成视频已经下载。补充文件按 `<case-id>_<用途>` 命名，例如 `assets/refs/K1_speech.mp4`、`assets/targets/K1_reference.mp4`。

K3 已备 [错误字幕样本](assets/refs/K3_subtitles_bad.srt) 和 [评测答案](assets/refs/K3_expected_issues.json)。这是无配套音频的人工结构样本，只覆盖可由字幕结构判断的规则；语音不匹配、无声/漏字幕、同音字和剪辑点检查仍需真实素材。答案只给评测方，不发给被测模型。

后续新场景复制 `cases/_template`，本表继续追加；这10项不限制后续测试范围。

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
│   │   ├── case.yaml            # 来源、准备清单、交互步骤、输出规格、验收
│   │   └── prompt.md            # 喂给模型的 prompt
│   ├── K1/                     # 口播信息卡
│   ├── K2/                     # 口播讲解动画
│   ├── K3/                     # 字幕质检
│   ├── P1/                     # UI卡拍循环
│   ├── P2/                     # 换品牌复刻
│   ├── P3/                     # 网站3D飞越
│   ├── T1/                     # 六文件功能教程
│   ├── T2/                     # 七段式竖屏教程
│   ├── L1/                     # 视频方法学习
│   └── L2/                     # 仅链接视频复刻
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
    └── registry.yaml            # skill来源、固定commit、本机入口、候选与依赖
```
<!-- TREE:END -->

## 各目录一句话

| 目录 | 放什么 |
|---|---|
| `models/` | 模型接入信息与默认参数，一个 YAML 搞定 |
| `cases/` | 每个场景两个文件：case.yaml 和 prompt.md |
| `assets/` | 跨用例复用的目标视频与参考素材 |
| `outputs/<run_id>/` | 单次任务的全部产物，绝不跨任务混用 |
| `runs/RUNS.md` | 台账，唯一索引；找不到产物先查这里 |
| `scripts/` | 三个脚本：建 run / 调模型 / 校验目录 |
| `skills/` | 外部 skill 登记；大体积源码安装在本机全局技能目录 |

## 命名规范

- `run_id` = `YYYYMMDD-HHMMSS_<model>_<case>`（Asia/Shanghai）
- 视频文件名以 run_id 开头：`<run_id>_v1.mp4`
- 同一次任务重跑就新建 run_id，不覆盖旧目录
- 客户素材加 `cust_` 前缀，视为敏感数据

## 每次任务的规则

1. 先读本 README「测试场景」「目录结构」+ [RUNS.md](runs/RUNS.md) 末尾几行，再由测试操作者检查对应 `case.yaml`。
2. 实际测试目录用 `new_run.py` 生成。只做准备时，不建模型run、不调用接口、不产生视频；台账记录为准备完成。
3. 新增/删除目录后更新本 README 目录树，跑 `python3 scripts/check_tree.py` 直到通过。
4. 新模型加到 `models.yaml`，新用例复制 `cases/_template`，新 skill 记到 `skills/registry.yaml`。
5. 密钥只放 `models/.env`。
6. 被测模型只接收 `prompt.md`、指定输入及必要技能；验收答案和隐藏的参考说明留给评测方。L1仅交学习卡，K3先报告再改；各场景按自己的确认点执行。
7. 不把可获取的教学素材或合成样本混作客户输入；缺项明示。实际运行时将使用的prompt、输入路径/哈希、skill commit、用户各轮反馈归档，两个模型保持一致。

## 技能与环境

[registry.yaml](skills/registry.yaml) 登记 dashi-animationstyle 和官方 remotion-best-practices 的固定 commit 与本机入口。后续 Agent 显式读取入口；从 GitHub 换一台机器后需按登记版本重新准备。本次不启动技能自带的示例、Studio、渲染器或模型调用。

T1 文档没有指定 motion-design-skill 仓库，LottieFiles 的同名仓库只是已核实的候选，尚未安装或当作原版使用。

2026-10-29 本机只读检查：macOS arm64，Python 3.9.6、Node 25.8.2、npm 11.11.1、ffmpeg/ffprobe 8.1.2 和 Chrome 已存在；本次 Python 环境缺 numpy/scipy，未找到 whisper CLI。dashi 有「逐字稿+静音检测」后备对齐，但不能计为精确ASR。Geist、Instrument Serif、思源黑体及按需系统字体尚未验证。正式运行各工程再固定依赖和浏览器版本。

## 怎么评

- 视频硬门槛：能播、时长/分辨率/fps符合case、信息点无错字、无水印。K3按问题检出和修改范围验收；L1按学习卡验收，不能因没有视频判失败。
- 打分：内容准确性、视觉质量、节奏、参考还原度、代码可复现性，1-5 分。
- 结论写一行进 RUNS.md：`pass 4.2/5 | 优于 baseline 12% | 问题：结尾空镜过长`。

## 备注

- API key 只在 `models/.env`（已 gitignore），仓库里只有 `.env.example`。
- 视频/图片等大文件默认不入库；要入库请换 Git LFS。
