"""
Beta-test simulation: 50 synthetic users interact with the recommender API.
"""
import os
import random
import requests
import pandas as pd

API_URL = os.getenv("STYLEMI_API_URL", "http://localhost:8000")
N_USERS = 50
OCCASIONS = ["casual", "formal", "athletic", "evening", "business", "party"]
CITIES = ["New York", "London", "Tokyo", "Mumbai", "Paris"]


def run():
    results = []
    for uid in range(1, N_USERS + 1):
        occ = random.choice(OCCASIONS)
        city = random.choice(CITIES)
        try:
            r = requests.post(
                f"{API_URL}/api/recommend/",
                json={"user_id": uid, "occasion": occ, "city": city, "top_k": 5},
                timeout=15,
            )
            if not r.ok:
                continue
            recs = r.json()["recommendations"]
        except Exception:
            continue

        clicked = random.random() < 0.4
        rating = random.choices([5, 4, 3, 2, 1], weights=[0.25, 0.30, 0.25, 0.12, 0.08])[0]
        for rec in recs[:1]:
            try:
                requests.post(
                    f"{API_URL}/api/feedback/",
                    json={"user_id": uid, "outfit_id": rec["outfit_id"],
                          "rating": rating, "liked": clicked},
                    timeout=10,
                )
            except Exception:
                pass
        results.append({"user": uid, "occasion": occ, "city": city,
                        "clicked": clicked, "rating": rating,
                        "avg_score": sum(r["score"] for r in recs) / max(len(recs), 1)})

    df = pd.DataFrame(results)
    os.makedirs("ml_pipeline/results", exist_ok=True)
    df.to_csv("ml_pipeline/results/beta_simulation.csv", index=False)
    summary = {
        "users": len(df),
        "ctr": float(df["clicked"].mean()) if len(df) else 0.0,
        "avg_rating": float(df["rating"].mean()) if len(df) else 0.0,
        "avg_score": float(df["avg_score"].mean()) if len(df) else 0.0,
    }
    print(summary)
    pd.DataFrame([summary]).to_csv("ml_pipeline/results/beta_summary.csv", index=False)


if __name__ == "__main__":
    run()
