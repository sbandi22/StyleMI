"""
CLIP image encoder. Wraps OpenAI CLIP ViT-B/32 for 512-dim embeddings.
Falls back to a deterministic hash-based embedding if torch/CLIP can't load.
"""
import numpy as np
from PIL import Image
import hashlib

try:
    import torch
    import clip
    _CLIP_AVAILABLE = True
except Exception:
    _CLIP_AVAILABLE = False


class CLIPEncoder:
    def __init__(self, model_name: str = "ViT-B/32"):
        self.available = _CLIP_AVAILABLE
        if self.available:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model, self.preprocess = clip.load(model_name, device=self.device)
            self.model.eval()

    def encode_image(self, image_path: str) -> np.ndarray:
        if self.available:
            image = self.preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to(self.device)
            with torch.no_grad():
                feats = self.model.encode_image(image)
            v = feats.cpu().numpy().flatten()
            return v / (np.linalg.norm(v) + 1e-9)
        with open(image_path, "rb") as f:
            digest = hashlib.sha256(f.read()).digest()
        rng = np.random.default_rng(int.from_bytes(digest[:8], "big"))
        v = rng.standard_normal(512).astype("float32")
        return v / (np.linalg.norm(v) + 1e-9)

    def encode_text(self, text: str) -> np.ndarray:
        if self.available:
            tokens = clip.tokenize([text]).to(self.device)
            with torch.no_grad():
                feats = self.model.encode_text(tokens)
            v = feats.cpu().numpy().flatten()
            return v / (np.linalg.norm(v) + 1e-9)
        rng = np.random.default_rng(abs(hash(text)) % (2**32))
        v = rng.standard_normal(512).astype("float32")
        return v / (np.linalg.norm(v) + 1e-9)
