import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageDraw
from PyPDF2 import PdfMerger

# 日本語フォントを設定
plt.rcParams["font.family"] = "MS Gothic"  # Windows用フォント（Mac/Linuxでは適切なフォントを設定）

# lineカラムの範囲を指定（例として6つの範囲）
ranges = [
    (1, 8),
    (9, 23),
    (24, 50),
    (51, 66),
    (67, 81),
    (82, 149)
]

# データのパス
data_dir = "data/行列時系列/"
score_file = "data/q_score.csv"
output_dir = "data/クラスごとの注視時間割合/"
os.makedirs(output_dir, exist_ok=True)

# 被験者名と問題番号のリスト
subjects = [f"{prefix}_{i}" for prefix in ["A", "B", "C"] for i in range(3, 15)]
questions = ["q1", "q2", "q3", "q4_1", "q4_2", "q5"]

# 被験者絞り込みの切り替え変数
filter_subjects = True  # True: 被験者を絞り込む, False: 全出力

# 採点結果を読み込む
scores = pd.read_csv(score_file)

# PDFファイル作成
time_ratio_allq = {}
for question in questions: #問題ループ
    for correctness in ["正解", "不正解"]: #正誤ループ
        # PDFのマージに使用するオブジェクト
        time_ratio = []
        for subject in subjects: #被験者ループ
            # プログラムミスを除外
            if filter_subjects and question in ["q2", "q3"]:
                subject_prefix, subject_num = subject.split("_")
                if int(subject_num) < 9:  # 9未満の被験者はスキップ
                    continue
            
            # q4の小問の処理
            if question in ["q4_1", "q4_2"]:
                file_path = os.path.join(data_dir, f"{subject}-q4.csv")
            else:
                file_path = os.path.join(data_dir, f"{subject}-{question}.csv")
            
            if not os.path.exists(file_path):
                continue
            
            # 視線データを読み込む
            gaze_data = pd.read_csv(file_path)
            
            # `line` の値がマイナスの場合を `NaN` に置き換え
            gaze_data["line"] = gaze_data["line"].apply(lambda x: x if x >= 0 else float('nan'))
            
            # 採点結果を取得
            correct = scores.loc[scores["name"] == subject, question].values[0]
            

            # 各範囲に該当する行番号を格納する配列
            line_indices = [[] for _ in range(len(ranges))]

            # 各行についてlineカラムの値を確認
            for index, row in gaze_data.iterrows():
                for i, (lower, upper) in enumerate(ranges):
                    if lower <= row['line'] < upper:
                        line_indices[i].append(index)
            
            # 各範囲について、timeカラムの差分を計算
            time_differences = [[] for _ in range(len(ranges))]
            
            for i, indices in enumerate(line_indices):
                for index in indices:
                    if index > 0:  # インデックスが0の場合は比較できないためスキップ
                        time_diff = gaze_data.loc[index, "time"] - gaze_data.loc[index - 1, "time"]
                        time_differences[i].append(time_diff)
                
            # time_differencesの各要素配列の合計を計算し、新しい配列に格納
            time_sums = [sum(diffs) for diffs in time_differences]
            time_sums = time_sums / sum(time_sums)
            
            #注視時間割合配列の末尾に正誤ラベルを追加
            time_sums = time_sums.tolist()
            time_sums.append(correct)
            
            time_ratio.append(time_sums)
            
        time_ratio_allq[question] = time_ratio


#計算した時間割合をcsvに書き込み
for q, ratio_array in time_ratio_allq.items():
    df = pd.DataFrame(ratio_array)
    
    output_path = output_dir + q + ".csv"
    df.to_csv(output_path, index=False, header=False)


