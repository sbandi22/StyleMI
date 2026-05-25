"""Cosine similarity helpers operating on CLIP embeddings."""
import numpy as np
from typing import List


def cosine(a: List[float], b: List[float]) -> float:
    va, vb = np.array(a, dtype="float32"), np.array(b, dtype="float32")
    n = (np.linalg.norm(va) * np.linalg.norm(vb)) + 1e-9
    return float(np.dot(va, vb) / n)


def top_k_similar(query: List[float], corpus: List[List[float]], k: int = 5) -> List[int]:
    sims = [cosine(query, c) for c in corpus]
    return list(np.argsort(sims)[::-1][:k])
