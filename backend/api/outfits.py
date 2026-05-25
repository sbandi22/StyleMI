"""
Outfit upload, retrieval and listing endpoints.
"""
import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.db import get_db
from database.models import Outfit
from config import settings
from ml.clip_encoder import CLIPEncoder
from ml.color_analyzer import extract_dominant_colors
from utils.image_processor import save_image, validate_image
from utils.validators import validate_occasion

router = APIRouter()
encoder = CLIPEncoder()


@router.post("/upload")
async def upload_outfit(
    file: UploadFile = File(...),
    occasion: str = Form("casual"),
    season: str = Form("all"),
    user_id: int = Form(1),
    db: AsyncSession = Depends(get_db),
):
    """Upload an outfit image, extract embedding + color palette, persist to DB."""
    validate_occasion(occasion)
    contents = await file.read()
    validate_image(contents, settings.MAX_UPLOAD_SIZE_MB)

    filename = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(settings.UPLOAD_DIR, filename)
    save_image(contents, path)

    embedding = encoder.encode_image(path).tolist()
    colors = extract_dominant_colors(path, k=5)

    outfit = Outfit(
        user_id=user_id,
        filename=filename,
        image_path=path,
        occasion=occasion,
        season=season,
        embedding=embedding,
        dominant_colors=colors,
        tags=[occasion, season],
    )
    db.add(outfit)
    await db.commit()
    await db.refresh(outfit)
    return {"id": outfit.id, "filename": filename, "colors": colors}


@router.get("/{outfit_id}")
async def get_outfit(outfit_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Outfit).where(Outfit.id == outfit_id))
    outfit = res.scalar_one_or_none()
    if not outfit:
        raise HTTPException(404, "Outfit not found")
    return {
        "id": outfit.id,
        "filename": outfit.filename,
        "occasion": outfit.occasion,
        "season": outfit.season,
        "dominant_colors": outfit.dominant_colors,
        "tags": outfit.tags,
    }


@router.get("/")
async def list_outfits(db: AsyncSession = Depends(get_db), limit: int = 50):
    res = await db.execute(select(Outfit).limit(limit))
    items = res.scalars().all()
    return [{"id": o.id, "occasion": o.occasion, "filename": o.filename} for o in items]
