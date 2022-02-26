import os
import pandas as pd
import numpy as np
from glob import glob

def main():
    if not os.path.exists("results"):
        os.mkdir("results")

    data_root = "/home/fanqiliang/data/yidong"
    annotation = os.path.join(data_root, "Day8_0-54.txt")

    dt = pd.read_csv(annotation)

    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for file in glob(os.path.join("output", "*.txt")):
        _m_id = os.path.splitext(os.path.basename(file))[0]
        p_value = []
        for line in open(file, "r"):
            a, b = line.split(",")
            try:
                p_value.append([float(a), float(b)])
            except:
                p_value.append([np.nan, np.nan])
        p_value = np.asarray(p_value)

        p_idx = list(set(np.where(np.isnan(p_value))[0]))
        m_dt = dt[dt["machine_id"] == _m_id]

        kpi_ids = dt["kpi_id"].to_list()
        labels = dt["label"].to_list()

        for kpi_id, label in zip(kpi_ids, labels):
            if kpi_id not in p_idx and label == 1:
                TN += 1
            elif kpi_id not in p_idx and label == 0:
                FN += 1
            elif kpi_id in p_idx and label == 1:
                TP += 1
            else:
                FP += 1
    
    print(f"TP: {TP}, FP: {FP}, TN: {TN}, FN: {FN}")
    print("recall: ", TP / (TP + FN))
    print("precision: ", TP / (TP + FP))

if __name__ == "__main__":
    main()
