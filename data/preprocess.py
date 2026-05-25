"""Preprocess raw images: resize, normalize, save to backend/uploads."""
import os
from PIL import Image

SRC = "data/sample/images"
DST = "backend/uploads"
SIZE = (512, 512)


def main():
    os.makedirs(DST, exist_ok=True)
    n = 0
    for fname in os.listdir(SRC):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        img = Image.open(os.path.join(SRC, fname)).convert("RGB")
        img.thumbnail(SIZE)
        img.save(os.path.join(DST, fname), quality=90)
        n += 1
    print(f"Preprocessed {n} images -> {DST}")


if __name__ == "__main__":
    main()
