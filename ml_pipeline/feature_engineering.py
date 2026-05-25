"""
Feature engineering pipeline.
Builds a tabular feature matrix from outfit metadata + CLIP embeddings.
"""
import os
import json
import pandas as pd
import numpy as np


def build_feature_frame(outfits: list) -> pd.DataFrame:
    rows = []
    for o in outfits:
        emb = np.array(o.get("embedding") or [0.0] * 8)
        rows.append({
            "id": o["id"],
            "occasion": o.get("occasion", "casual"),
            "season": o.get("season", "all"),
            "emb_mean": float(np.mean(emb)),
            "emb_std": float(np.std(emb)),
            "n_colors": len(o.get("dominant_colors") or []),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df = pd.get_dummies(df, columns=["occasion", "season"], drop_first=False)
    return df


if __name__ == "__main__":
    sample = json.load(open("data/sample/outfits.json"))
    df = build_feature_frame(sample)
    os.makedirs("ml_pipeline/results", exist_ok=True)
    df.to_csv("ml_pipeline/results/features.csv", index=False)
    print(df.head())
