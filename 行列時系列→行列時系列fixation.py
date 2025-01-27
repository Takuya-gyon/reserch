import pandas as pd
import numpy as np
import os

# 入力フォルダと出力フォルダの指定
input_folder = './data/行列時系列'
fixation_output_folder = './data/行列時系列fixation'
velocity_output_folder = './data/行列時系列速度付き'

# 出力フォルダが存在しない場合は作成
os.makedirs(fixation_output_folder, exist_ok=True)
os.makedirs(velocity_output_folder, exist_ok=True)

# フォルダ内のすべてのCSVファイルを処理
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        input_path = os.path.join(input_folder, file_name)
        fixation_output_path = os.path.join(fixation_output_folder, file_name.replace('.csv', '_fixation.csv'))
        velocity_output_path = os.path.join(velocity_output_folder, file_name.replace('.csv', '_velocity.csv'))

        # CSVファイルの読み込み
        data = pd.read_csv(input_path)

        # 時間差を計算
        data['time_diff'] = data['time'].diff()

        # 座標差を計算
        data['x_diff'] = data['x'].diff()
        data['y_diff'] = data['y'].diff()

        # ユークリッド距離を計算
        data['distance'] = np.sqrt(data['x_diff']**2 + data['y_diff']**2)

        # 速度情報付きデータを保存
        data.to_csv(velocity_output_path, index=False)

        # 20個前のデータとの行列距離を計算
        data['prev_line'] = data['line'].shift(20)
        data['prev_col'] = data['col'].shift(20)
        data['distance_from_prev'] = np.sqrt((data['line'] - data['prev_line'])**2 + (data['col'] - data['prev_col'])**2)

        # 距離が20以上のデータをフィルタリング
        filtered_data = data.copy()
        filtered_data.loc[filtered_data['distance_from_prev'] >= 10, ['x', 'y', 'line', 'col', 'distance', 'distance_from_prev']] = np.nan

        # フィルタリングしたデータをCSVに保存
        filtered_data.to_csv(fixation_output_path, index=False)

print("すべてのファイルの処理が完了しました。")
