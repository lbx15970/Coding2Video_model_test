import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# 视频参数：30 FPS，共 90 帧，时长 3 秒
FPS = 30
FRAMES = 90

# 柱状图数据
categories = ["A", "B", "C", "D", "E"]
final_values = [25, 48, 36, 72, 58]
colors = ["#4C72B0", "#DD8452", "#55A467", "#C44E52", "#8172B3"]

# 创建画布
fig, ax = plt.subplots(figsize=(8, 4.5))

# 初始高度全部为 0
bars = ax.bar(
    categories,
    np.zeros(len(categories)),
    color=colors,
    edgecolor="white",
    linewidth=1.2
)

ax.set_ylim(0, max(final_values) * 1.15)
ax.set_ylabel("Value")
ax.set_title("3-Second Bar Chart Growth Animation")
ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)
fig.tight_layout()


def update(frame):
    """每帧更新柱子高度。"""
    progress = frame / (FRAMES - 1)  # 0.0 -> 1.0

    for bar, target_value in zip(bars, final_values):
        bar.set_height(target_value * progress)

    return bars


# 创建动画
animation = FuncAnimation(
    fig,
    update,
    frames=FRAMES,
    interval=1000 / FPS,
    blit=True
)

# 输出 MP4
writer = FFMpegWriter(
    fps=FPS,
    codec="libx264",
    extra_args=["-pix_fmt", "yuv420p"]
)

animation.save("smoke_v1.mp4", writer=writer, dpi=160)

print("已生成：smoke_v1.mp4")
