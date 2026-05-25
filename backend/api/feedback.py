"""Feedback collection - drives the preference-learning loop."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

from database.db import get_db
from database.models import Feedback
from ml.preference_learner import PreferenceLearner

router = APIRouter()
learner = PreferenceLearner()


class FeedbackIn(BaseModel):
    user_id: int
    outfit_id: int
    rating: int
    liked: bool = False
    comment: Optional[str] = None


@router.post("/")
async def submit_feedback(payload: FeedbackIn, db: AsyncSession = Depends(get_db)):
    fb = Feedback(
        user_id=payload.user_id,
        outfit_id=payload.outfit_id,
        rating=payload.rating,
        liked=payload.liked,
        comment=payload.comment,
    )
    db.add(fb)
    await db.commit()
    await learner.update_from_feedback(db, payload.user_id)
    return {"status": "recorded"}
