import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageDraw
from PyPDF2 import PdfMerger

# 日本語フォントを設定
plt.rcParams["font.family"] = "MS Gothic"  # Windows用フォント（Mac/Linuxでは適切なフォントを設定）

# データのパス
data_dir = "data/行列時系列/"
score_file = "data/q_score.csv"
background_image_path = "data/carbon_clip_resized.png"  # 背景画像のパス
output_dir = "output/行の時系列グラフプログラム背景/"
os.makedirs(output_dir, exist_ok=True)

# 被験者名と問題番号のリスト
subjects = [f"{prefix}_{i}" for prefix in ["A", "B", "C"] for i in range(3, 15)]
questions = ["q1", "q2", "q3", "q4_1", "q4_2", "q5"]

# 被験者絞り込みの切り替え変数
filter_subjects = True  # True: 被験者を絞り込む, False: 全出力

# 採点結果を読み込む
scores = pd.read_csv(score_file)

# PDFファイル作成
for question in questions: #問題ループ
    for correctness in ["正解", "不正解"]: #正誤ループ
        # PDFのマージに使用するオブジェクト
        merger = PdfMerger()
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
            
            # 正誤条件に一致しない場合はスキップ
            if (correctness == "正解" and correct == 0) or (correctness == "不正解" and correct == 1):
                continue
            
            # 縦軸の範囲設定（反転用に上下を逆に設定）
            """
            if question == "q1":
                y_min, y_max = 110, 84  # 反転のため上下を逆に
            elif question == "q2":
                y_min, y_max = 122, 110
            else:  # q3以降
                y_min, y_max = 149, 0
            """
            y_min, y_max = 149, 0
            
            
            # グラフ作成
            plt.figure(figsize=(8, 6))
            plt.plot(gaze_data["time"], gaze_data["line"], label="line",alpha=0.5, color="blue")
            plt.title(f"{subject} - {question} ({correctness})", fontsize=14)
            plt.xlabel("Time", fontsize=12)
            plt.ylabel("Line", fontsize=12)
            plt.ylim(y_min, y_max)  # 反転した縦軸の範囲を設定
            #plt.legend(fontsize=10)
            #plt.grid(True)
            
            # グラフを背景透過で保存
            graph_path = "temp/image/transparent_graph.png"
            plt.savefig(graph_path, transparent=True, bbox_inches='tight', dpi=300)
            plt.close()
            
            # Pillowで画像を合成
            background = Image.open(background_image_path).convert("RGBA")
            graph = Image.open(graph_path).convert("RGBA")
            w, h = background.size
            container = Image.new("RGBA", (w, h))
            
            # 背景画像にグラフを重ねる
            t = 0.838
            container.paste(background.resize((int(w * t), int(h * t))), (55, 168))
            container = Image.alpha_composite(container, graph.resize((w, h)))

            # 一時的にPDFとして保存
            temp_pdf = f"temp/pdf/temp_{subject} - {question}.pdf"
            container.save(temp_pdf, "PDF")
         
            # マージ用オブジェクトに追加
            merger.append(temp_pdf)
            
            # 各pdfにつき被験者１人だけ出す（テスト用）
            #break
                
        # PDFを結合して保存
        merger.write(f"{output_dir}{question}_{correctness}.pdf")
        merger.close()

print("PDFの生成が完了しました。")
