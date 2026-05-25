"""
Evaluation metrics for the recommender:
Precision@K, Recall@K, NDCG@K, plus a simple plot.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def precision_at_k(rel: list, k: int) -> float:
    return float(np.mean(rel[:k])) if rel else 0.0


def recall_at_k(rel: list, total_relevant: int, k: int) -> float:
    if total_relevant == 0:
        return 0.0
    return float(sum(rel[:k]) / total_relevant)


def ndcg_at_k(rel: list, k: int) -> float:
    rel = np.asarray(rel[:k], dtype="float32")
    if rel.size == 0:
        return 0.0
    discounts = 1.0 / np.log2(np.arange(2, rel.size + 2))
    dcg = float(np.sum(rel * discounts))
    ideal = float(np.sum(np.sort(rel)[::-1] * discounts))
    return dcg / ideal if ideal > 0 else 0.0


def save_plot(metrics: dict, out: str):
    plt.figure(figsize=(7, 4))
    plt.bar(list(metrics.keys()), list(metrics.values()))
    plt.title("StyleMI - Recommendation Accuracy")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(out, dpi=120)


if __name__ == "__main__":
    demo = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
    metrics = {
        "Precision@5": precision_at_k(demo, 5),
        "Recall@10": recall_at_k(demo, 6, 10),
        "NDCG@10": ndcg_at_k(demo, 10),
    }
    os.makedirs("ml_pipeline/results", exist_ok=True)
    pd.DataFrame({"metric": list(metrics), "value": list(metrics.values())}).to_csv(
        "ml_pipeline/results/metrics.csv", index=False
    )
    save_plot(metrics, "ml_pipeline/results/metrics.png")
    print(metrics)
