"""Generates a synthetic outfit dataset and 30 sample placeholder JPEGs."""
import os
import json
import random
import numpy as np
from PIL import Image

OUT_DIR = "data/sample"
IMG_DIR = os.path.join(OUT_DIR, "images")
N = 30
OCCASIONS = ["casual", "formal", "athletic", "evening", "business", "party"]
SEASONS = ["summer", "winter", "spring", "autumn", "all"]


def make_image(path):
    arr = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
    Image.fromarray(arr).save(path, "JPEG")


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    outfits = []
    for i in range(1, N + 1):
        fname = f"outfit_{i:03d}.jpg"
        make_image(os.path.join(IMG_DIR, fname))
        outfits.append({
            "id": i,
            "filename": fname,
            "occasion": random.choice(OCCASIONS),
            "season": random.choice(SEASONS),
            "embedding": np.random.randn(8).tolist(),
            "dominant_colors": [tuple(np.random.randint(0, 255, 3).tolist()) for _ in range(5)],
        })
    with open(os.path.join(OUT_DIR, "outfits.json"), "w") as f:
        json.dump(outfits, f, indent=2)
    print(f"Generated {N} sample outfits in {OUT_DIR}")


if __name__ == "__main__":
    main()
