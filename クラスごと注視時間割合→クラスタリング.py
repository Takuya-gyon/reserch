import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans

input_dir = "data/クラスごとの注視時間割合/"

questions = ["q3", "q4_2", "q5"]

result_allq = {}
for question in questions:
    df = pd.read_csv(input_dir + f"{question}.csv", header=None)
    
    vectors = df.iloc[:, :-1]
    labels = df.iloc[:, -1]
    
    # K-meansクラスタリング
    n_clusters = 2  # クラスタの数
    kmeans = KMeans(n_clusters=n_clusters, random_state=4)
    kmeans.fit(vectors)
    
    # クラスタリング結果のラベルを取得
    clusters = kmeans.labels_
    df["clusters"] = clusters
    
    result_allq[question] = df
    
    print("クラスタリング結果:")
    print(df.iloc[:, -2:])