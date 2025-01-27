import numpy as np
import pandas as pd
import os
import xml.etree.ElementTree as ET

BASE_DIR = ".//data//12月分生xml"

for folder in ["A", "B", "C"]:
    folder_path = os.path.join(BASE_DIR, folder)
    if not os.path.isdir(folder_path):
        continue

    # 3～14フォルダを探索
    for subfolder in range(3, 15):  # 3～14の範囲
        subfolder_path = os.path.join(folder_path, str(subfolder))
        if not os.path.isdir(subfolder_path):
            continue
        
        # XMLファイルを取得
        files = []
        for file in os.listdir(subfolder_path):
            if(not "itrace_atom" in file):
                continue
            
            files.append(file)
        
        files.sort()
        
        folder_label = f"{folder}_{subfolder}"
        
        count = 0
        if(folder_label == "C_10"):
            count += 1
            
        for file in files:
            file_path = os.path.join(subfolder_path, file)
            print(f'file:{folder_label}/{file}')
            
            #xmlファイル読み込み
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Extract gaze data
            gazes = root.find("gazes")
            gaze_data = []
            
            if gazes is not None:
                for response in gazes.findall("response"):
                    print(f'time:{response.get("plugin_time")}')
                    time = int(response.get("plugin_time")) - int(file.split('-')[-1][:-4])
                    x = int(response.get("x"))
                    y = int(response.get("y"))
                    line = int(response.get("source_file_line"))
                    col = int(response.get("source_file_col"))
            
                    gaze_data.append((time, x, y, line, col))
            
            df = pd.DataFrame(gaze_data, columns=["time", "x", "y", "line", "col"])
            
            df.to_csv(f".//data//行列時系列//{folder_label}-q{count}.csv", index=False)
            
            count += 1