import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import plotly.graph_objects as go

# 日本語フォントを設定
#plt.rcParams["font.family"] = "MS Gothic"  # Windows用フォント（Mac/Linuxでは適切なフォントを設定）

# サンプルの6次元データを生成
input_dir = "data/クラスごとの注視時間割合/"

questions = ["q3", "q4_1", "q4_2", "q5"]

for question in questions:
    #データ読み込み
    df = pd.read_csv(input_dir + f"{question}.csv", header=None)
    data = df.iloc[:, :-1]
    labels = df.iloc[:, -1:].iloc[:, 0]
    
    # 主成分分析（PCA）で3次元に次元削減
    pca = PCA(n_components=3)
    data_3d = pca.fit_transform(data)
    # 累積寄与率を計算
    explained_variance_ratio = pca.explained_variance_ratio_  # 各主成分の寄与率
    cumulative_explained_variance = np.sum(explained_variance_ratio)  # 累積寄与率
    
    # ラベルごとの色設定
    colors = ['red', 'blue', 'green']  # ラベル0, 1, 2に対応する色
    label_names = ['不正解', '正解', '惜しい']  # ラベルの名前
    # 3Dプロットの作成
    fig = go.Figure()
    for i, color in enumerate(colors):
        mask = labels == i
        fig.add_trace(go.Scatter3d(
            x=data_3d[mask, 0],
            y=data_3d[mask, 1],
            z=data_3d[mask, 2],
            mode='markers',
            marker=dict(size=5, color=color),
            name=label_names[i]
        ))
    # 軸ラベルとタイトルを設定
    fig.update_layout(
        title=f'{question} (累積寄与率： {cumulative_explained_variance:.2%})',
        scene=dict(
            xaxis_title='Principal Component 1',
            yaxis_title='Principal Component 2',
            zaxis_title='Principal Component 3'
        )
    )
    
    # HTMLファイルに保存
    output_file = f"output/主成分分析3dグラフ/{question}.html"
    fig.write_html(output_file)
    
    print(f"インタラクティブな3Dプロットが {output_file} に保存されました。")

