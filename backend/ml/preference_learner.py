"""
Implicit preference learner. Updates per-user ensemble weights from feedback.
"""
import numpy as np
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Feedback, Preference
from config import settings


class PreferenceLearner:
    def __init__(self, lr: float = 0.05):
        self.lr = lr

    async def update_from_feedback(self, db: AsyncSession, user_id: int) -> None:
        res = await db.execute(select(Feedback).where(Feedback.user_id == user_id))
        feedbacks = res.scalars().all()
        if not feedbacks:
            return

        res = await db.execute(select(Preference).where(Preference.user_id == user_id))
        pref = res.scalar_one_or_none()
        if pref is None:
            pref = Preference(user_id=user_id, learned_weights=list(settings.ENSEMBLE_WEIGHTS))
            db.add(pref)

        weights = np.array(pref.learned_weights or settings.ENSEMBLE_WEIGHTS, dtype="float32")
        avg_rating = float(np.mean([f.rating for f in feedbacks]))
        delta = (avg_rating - 3.0) / 5.0
        weights[0] = max(0.05, weights[0] + self.lr * delta)
        weights[1] = max(0.05, weights[1] - self.lr * delta)
        weights = weights / weights.sum()
        pref.learned_weights = weights.tolist()
        await db.commit()
