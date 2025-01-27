import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# データのパス
background_image_path = "data/Main_reverse2.png"  # 背景画像のパス
output_image_path = "output/overlay_graph.png"  # 出力画像のパス

# 仮のデータフレーム作成
data = pd.DataFrame({
    "time": [0, 1, 2, 3, 4, 5],
    "line": [10, 12, 15, 14, 13, 11]
})

# グラフ作成（背景透過で保存）
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(data["time"], data["line"], color="blue", linewidth=2, label="Line")
ax.set_title("Sample Transparent Graph")
ax.set_xlabel("Time")
ax.set_ylabel("Line")
ax.invert_yaxis()
ax.legend()
plt.grid(True, alpha=0.5)

# グラフを背景透過で保存
graph_path = "output/transparent_graph.png"
plt.savefig(graph_path, transparent=True, bbox_inches='tight', dpi=300)
plt.close()

# Pillowで画像を合成
background = Image.open(background_image_path)
graph = Image.open(graph_path).convert("RGBA")
w, h = graph.size
container = Image.new("RGBA", (w, h), 0)

# 背景画像にグラフを重ねる
out_image = container.paste(background)
out_image = Image.alpha_composite(container, graph)

# 合成結果を保存または表示
out_image.save(output_image_path)
out_image.show()
