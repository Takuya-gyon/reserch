import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

plt.rcParams['font.family'] = 'MS Gothic' # Fonts

#正誤情報の読み込み
point_list = pd.read_csv(".//data//q_score.csv")

# データが保存されているフォルダのパス
data_folder = ".//data//行列時系列fixation"

#出力先フォルダ
output_folder = ".//output//行の時系列グラフfixation//"

# 人名と問題番号の範囲
#names = [f"A_{i}" for i in range(3, 15)] + [f"B_{i}" for i in range(3, 15)] + [f"C_{i}" for i in range(3, 15)]
questions = ["q1", "q2", "q3", "q4", "q5"]

#点数分け
point0 = {}
point1 = {}

q_list = ["q1", "q2", "q3", "q4_1", "q4_2", "q5"]

for q in q_list:
    point0[q] = np.array(point_list[point_list[q] == 0]["name"])
    point1[q] = np.array(point_list[point_list[q] == 1]["name"])
    

# PDFを作成する関数
def create_question_pdf2(data_folder, questions, pointN, ifCorrect=False):
    pdf_filename = output_folder + f"output2_{'正解者' if ifCorrect else '不正解者'}_fixation.pdf"
    with PdfPages(pdf_filename) as pdf:
        for question_label in questions:
            plt.figure(figsize=(10, 6))
            
            names = pointN.get(question_label)
            question = question_label
            
            if "q4" in question:
                question = "q4"
                
            for name in names:
                file_path = os.path.join(data_folder, f"{name}-{question}_fixation.csv")
                
                if os.path.exists(file_path):
                    # CSV読み込み
                    data = pd.read_csv(file_path)
                    
                    # 時系列データを仮定しているため、データが 'time', 'value' を持っていると仮定
                    if 'time' in data.columns and 'line' in data.columns:
                        # 負の値を無視する
                        data['line'] = data['line'].apply(lambda x: x if x >= 0 else float('nan'))
                        plt.plot(data['time'], data['line'], label=name)
                    else:
                        print(f"Invalid columns in file: {file_path}")
                        continue
                else:
                    print(f"File not found: {file_path}")

            # グラフの設定
            plt.title(f"Data for {question_label} {'正解者' if ifCorrect else '不正解者'}")
            plt.xlabel("Time")
            plt.ylabel("Value")
            plt.legend(loc="upper right", fontsize="small")
            plt.axhspan(9, 23, color="yellow", alpha=0.3)
            plt.axhspan(51, 66, color="yellow", alpha=0.3)
            plt.axhspan(1, 8, color="gray", alpha=0.3)
            plt.axhspan(24, 50, color="gray", alpha=0.3)
            plt.axhspan(67, 81, color="gray", alpha=0.3)
            plt.axhspan(12, 15, color='red', alpha=0.5)
            plt.axhspan(54, 57, color='red', alpha=0.5)
            
            if "q1" in question:
                plt.ylim(85, 108)
            if "q2" in question:
                plt.ylim(111, 120)
            plt.grid(True)

            # PDFにページを追加
            pdf.savefig()
            plt.close()

# プログラムの実行
if __name__ == "__main__":
    create_question_pdf2(data_folder, q_list, point0, False)
    create_question_pdf2(data_folder, q_list, point1, True)
    print("PDFファイルの作成が完了しました。")
