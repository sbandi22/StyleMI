"""
Recommendation endpoints - ensemble scoring using CLIP, color, weather and CF signals.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional

from database.db import get_db
from database.models import History
from ml.recommender import EnsembleRecommender

router = APIRouter()
recommender = EnsembleRecommender()


class RecommendRequest(BaseModel):
    user_id: int
    occasion: str = "casual"
    city: Optional[str] = "New York"
    top_k: int = 5
    seed_outfit_id: Optional[int] = None


@router.post("/")
async def recommend(req: RecommendRequest, db: AsyncSession = Depends(get_db)):
    """Return top-k outfit recommendations and persist to history."""
    results = await recommender.recommend(
        db=db,
        user_id=req.user_id,
        occasion=req.occasion,
        city=req.city,
        top_k=req.top_k,
        seed_outfit_id=req.seed_outfit_id,
    )
    history = History(
        user_id=req.user_id,
        recommended_ids=[r["outfit_id"] for r in results],
        context={"occasion": req.occasion, "city": req.city},
        score=sum(r["score"] for r in results) / max(len(results), 1),
    )
    db.add(history)
    await db.commit()
    return {"recommendations": results}


@router.get("/history/{user_id}")
async def get_history(user_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        select(History).where(History.user_id == user_id).order_by(History.created_at.desc())
    )
    rows = res.scalars().all()
    return [
        {
            "id": h.id,
            "recommended_ids": h.recommended_ids,
            "context": h.context,
            "score": h.score,
            "created_at": h.created_at.isoformat(),
        }
        for h in rows
    ]
