# P1｜一个形状变遍所有 UI 的卡拍循环动效

做一支 14 秒、1440×1440 的 UI 动效。状态依次是：按钮、加载、对勾、灵动岛、音乐播放器、进度条、音量滑块、开关、标签页、图表、⌘K 搜索、弹窗提示，最后回到按钮。配色纯黑白，音乐使用 `assets/refs/P1_music.wav`，约 120 BPM。

<direction>
Dribbble-level UI motion. One shape, never cut: every state is the same element morphing its size, radius and color while its content swaps with a short blur. A cursor drives every change with real clicks and drags. Light warm-gray canvas, black and white components, one clean UI font (Geist). Springs everywhere, a tiny overshoot at most. The camera zooms so each state fills the frame. The last frame is the first frame, so it loops.
Banned: bouncy easing, particle bursts, glows, gradients on UI chrome, mismatched icon strokes, dead time, anything that looks like a template.
</direction>

120 BPM 一拍约 0.5 秒，14 秒约 28 拍。先列出各状态和动作占用哪些拍，不要误把 12 个状态简单均分成 14 秒；音乐实际节拍以分析结果为准。

当前这是基于已读场景和 direction 的整理版，不是完整原长 prompt。先补齐原 prompt 的未读细项并确认帧率、音乐与字体，再确认时间线，之后才执行生成。

检查 `t=0` 与循环边界的形状、光标、镜头和内部内容是否连续。最终视频保存为 `outputs/<run_id>/videos/<run_id>_v1.mp4`。
