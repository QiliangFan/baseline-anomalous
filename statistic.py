
"""
分数中出现NA,主要是输入的时间序列的值都一样.因此对于Na可直接看作是1(正常序列)
"""

import numpy as np
import pandas as pd
import os
from glob import glob
from sklearn.metrics import precision_recall_curve



def main(label_file: str, output_root: str):
    label = pd.read_csv(label_file, dtype=int)
    label = pd.concat([label, pd.DataFrame({"score": []})], ignore_index=True)
    label = pd.concat([label, pd.DataFrame({"pred_label": []})], ignore_index=True)

    results = glob(os.path.join(output_root, "*.txt"))


    # 首先收集所有分数，根据最优F1-score确定阈值
    for result in results:
        dt = pd.read_csv(result)
        m_id = int(os.path.basename(result).split(".")[0])
        for kpi_id, (idx, (sc1, sc2)) in enumerate(dt.iterrows()):
            row_num = label[(label["machine_id"] == m_id) & (label["kpi_id"] == kpi_id)].index[0]
            score = np.mean([sc1, sc2])
            label.at[row_num, "score"] = score
    
    scores = label["score"].values
    labels = label["label"].values
    non_nan_idx = np.where(~np.isnan(scores))
    scores = scores[non_nan_idx]
    scores = (scores - scores.min()) / (scores.max() - scores.min())
    
    labels = labels[non_nan_idx]
    labels = np.where(labels == 2, 1, 0)

    precision, recall, th = precision_recall_curve(labels, - scores)
    f1 = 2 * precision * recall / (precision + recall + 1e-6)
    best_f1_idx = np.argmax(f1)

    best_f1_corr_th = th[best_f1_idx]
    
    TOTAL = 0
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for idx, row in label.iterrows():
        score = row["score"]
        if np.isnan(score):
            pred_label = 1
        elif score >= best_f1_corr_th:
            pred_label = 2
        else:
            pred_label = 1
        label.at[idx, "pred_label"] = pred_label
        tag = label.at[idx, "label"]
        tag = 1 if tag == 1 else 2

        if tag == 2:
            if pred_label == tag:
                TP += 1
            else:
                FN += 1
        else:
            if pred_label == tag:
                TN += 1
            else:
                FP += 1
        TOTAL += 1
    
    print(f"           {output_root}           ")
    print("============== STAT ===============")
    print(f"TP:{TP:<8d}FN:{FN:<8d}")
    print(f"TN:{TN:<8d}FP:{FP:<8d}")
    precision = TP/(TP+FP)
    print(f"Recall:{precision:<16}")
    recall = TP/(TP+FN)
    print(f"Precision:{recall}")
    print(f"f1:{2*precision*recall/(precision+recall)}")
    print(f"TOTAL:{TOTAL:>8d}")
    print("=============== END ===============")

    label = label.convert_dtypes()
    # machine_id,kpi_id,label,pred_label
    label.to_csv(f"{output_root.split('_')[1]}_result.csv", index=False, columns=["machine_id", "kpi_id", "label", "pred_label"])


if __name__ == "__main__":
    # 移动Datasets
    if os.path.exists("output_yidong"):
        main(os.path.join("/home/fanqiliang/data/yidong", "label.csv"), "output_yidong")

    # 字节Datasets
    if os.path.exists("output_zijie"):
        main(os.path.join("/home/fanqiliang/data/OutSpotDataset", "Day35_0-199.csv"), "output_zijie")
