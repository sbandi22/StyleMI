"""
OpenCV-based color analysis: dominant palette extraction (k-means) and color harmony scoring.
"""
import cv2
import numpy as np
from typing import List, Tuple


def extract_dominant_colors(image_path: str, k: int = 5) -> List[Tuple[int, int, int]]:
    img = cv2.imread(image_path)
    if img is None:
        return []
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_small = cv2.resize(img, (128, 128))
    Z = img_small.reshape((-1, 3)).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(Z, k, None, criteria, 5, cv2.KMEANS_PP_CENTERS)
    centers = centers.astype(int)
    counts = np.bincount(labels.flatten(), minlength=k)
    order = np.argsort(-counts)
    return [tuple(int(c) for c in centers[i]) for i in order]


def rgb_to_hsv(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    arr = np.uint8([[list(rgb)]])
    hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV)[0][0]
    return float(hsv[0]) * 2.0, float(hsv[1]) / 255.0, float(hsv[2]) / 255.0


def color_harmony_score(colors_a: List[Tuple[int, int, int]],
                        colors_b: List[Tuple[int, int, int]]) -> float:
    """0..1 harmony - rewards complementary / analogous hue relationships."""
    if not colors_a or not colors_b:
        return 0.0
    score = 0.0
    pairs = 0
    for ca in colors_a[:3]:
        for cb in colors_b[:3]:
            ha, _, _ = rgb_to_hsv(ca)
            hb, _, _ = rgb_to_hsv(cb)
            d = min(abs(ha - hb), 360 - abs(ha - hb))
            best = min(abs(d - 180), abs(d - 30), abs(d - 120), abs(d - 0))
            score += max(0.0, 1.0 - best / 60.0)
            pairs += 1
    return float(score / pairs) if pairs else 0.0
