import os
import pandas as pd
import numpy as np
from glob import glob
from sklearn.metrics import f1_score, precision_recall_curve, roc_auc_score, roc_curve

def main():
    if not os.path.exists("results"):
        os.mkdir("results")

    data_root = "/home/fanqiliang/data/yidong"
    annotation = os.path.join(data_root, "Day8_0-54.txt")

    dt = pd.read_csv(annotation)
    scores = []
    labels = []

    file_list = glob(os.path.join("output", "*.txt"))
    file_list.sort(key = lambda v: int(os.path.splitext(os.path.basename(v))[0]))
    for file in file_list:
        _m_id = int(os.path.splitext(os.path.basename(file))[0])
        first = True
        fp = open(file, "r")
        for line in fp:
            if first: 
                first = False
                continue
            a, b = [v.strip() for v in line.split(",")]
            try:
                scores.append(np.mean([float(a), float(b)]))
            except:
                scores.append(np.nan)

        m_dt = dt[dt["machine_id"] == _m_id]
        m_dt = m_dt.sort_values(by="kpi_id")
        labels.extend(m_dt["label"].to_list())

    labels = 1 - np.asarray(labels)
    scores = np.asarray(scores)
    labels = labels[~np.isnan(scores)]
    scores = scores[~np.isnan(scores)]
    # scores = - np.where(np.isnan(scores), np.nanmax(scores) * np.ones_like(scores) + 1, scores)
    scores = (scores - scores.min()) / (scores.max() - scores.min())

    auc = roc_auc_score(labels, scores)
    precision, recall, th = precision_recall_curve(labels, scores)
    fpr, tpr, _ = roc_curve(labels, scores)

    # pr curve 
    result = pd.DataFrame({
        "predicion": precision,
        "recall": recall
    })
    result.to_csv("pr.csv", index=False)

    # roc
    result = pd.DataFrame({
        "tpr": tpr,
        "fpr": fpr
    })
    result.to_csv("roc.csv", index=False)

    f1_score = (2 * precision * recall) / (precision + recall)
    idx = np.nanargmax(f1_score)
    best_f1_score = f1_score[idx]
    best_precision = precision[idx]
    best_recall = recall[idx]

    print(f"auc: {auc} best_f1_score: {best_f1_score} best_precision: {best_precision} best_recall: {best_recall}")

    dt = pd.DataFrame({
        "labels": labels,
        "scores": scores
    })
    dt.to_csv("results.csv", index=False)

if __name__ == "__main__":
    main()
