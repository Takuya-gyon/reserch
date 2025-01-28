import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# サンプルの6次元データを生成
input_dir = "data/クラスごとの注視時間割合/"

questions = ["q3", "q4_2", "q5"]

for question in questions:
    #データ読み込み
    df = pd.read_csv(input_dir + f"{question}.csv", header=None)
    data = df.iloc[:, :-1]
    label = df.iloc[:, -1:]
    
    # 主成分分析（PCA）で3次元に次元削減
    pca = PCA(n_components=3)
    data_3d = pca.fit_transform(data)
    
    # 累積寄与率を計算
    explained_variance_ratio = pca.explained_variance_ratio_  # 各主成分の寄与率
    cumulative_explained_variance = np.sum(explained_variance_ratio)  # 累積寄与率
    
    # 結果の可視化
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    # 各データ点を散布図としてプロット
    ax.scatter(data_3d[:, 0], data_3d[:, 1], data_3d[:, 2], c='b', marker='o')
    
    # 軸ラベルを設定
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.set_zlabel('Principal Component 3')
    
    # 累積寄与率をタイトルに挿入
    plt.title(f'PCA: 6D to 3D Visualization (Cumulative Variance: {cumulative_explained_variance:.2%})')
    
    # グラフ表示
    plt.show()
