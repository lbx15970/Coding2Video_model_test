# K2｜给口播配讲解动画

读取 `skills/registry.yaml` 中固定版本的 dashi-animationstyle 及其本机入口。

用它给 `assets/refs/K2_speech.wav` 配全屏讲解动画，逐字稿为 `assets/refs/K2_transcript.txt`。使用该仓库 README 排在第 1 种的「立体卡通」风格：炭黑底、光面立体物件、杂志分栏；不要按 SKILL.md 里另一张表的排序选错风格。

1920×1080、30 fps，时长与口播相同，保留口播并带字幕。说到哪个关键词，对应词语和讲解动作就在那个时刻出现。画面全部用 HTML/Canvas 代码绘制，不用生图模型。

先给方案和分镜确认，再出 3 张静帧确认，之后才渲染整段。没有 ASR 时可以使用逐字稿和静音检测的后备方案，但要明确报告时间估计和误差，不能声称做了精确字级识别。

这次不运行技能自带的 Token 渲染示例。生成任务开始后，作品目录放 `outputs/<run_id>/code/`，最终视频放 `outputs/<run_id>/videos/<run_id>_v1.mp4`。
