"""Image validation, saving and preprocessing helpers."""
import os
from io import BytesIO
from PIL import Image

ALLOWED_FORMATS = {"JPEG", "JPG", "PNG", "WEBP"}


def validate_image(contents: bytes, max_mb: int = 10) -> None:
    if len(contents) > max_mb * 1024 * 1024:
        raise ValueError(f"Image exceeds {max_mb}MB limit")
    try:
        img = Image.open(BytesIO(contents))
        img.verify()
        if img.format.upper() not in ALLOWED_FORMATS:
            raise ValueError(f"Unsupported format: {img.format}")
    except Exception as e:
        raise ValueError(f"Invalid image: {e}")


def save_image(contents: bytes, path: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = Image.open(BytesIO(contents)).convert("RGB")
    img.thumbnail((1024, 1024))
    img.save(path, format="JPEG", quality=90)
    return path
