"""
Ensemble recommendation engine.
Score = w1*content + w2*collaborative + w3*weather + w4*color_harmony + w5*occasion_match
"""
from typing import Optional, List, Dict
import numpy as np
import httpx
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database.models import Outfit, Feedback, Preference
from ml.similarity import cosine
from ml.color_analyzer import color_harmony_score
from ml.weather_scorer import weather_score


class EnsembleRecommender:
    def __init__(self):
        self.default_weights = list(settings.ENSEMBLE_WEIGHTS)

    async def _get_weights(self, db: AsyncSession, user_id: int) -> List[float]:
        res = await db.execute(select(Preference).where(Preference.user_id == user_id))
        pref = res.scalar_one_or_none()
        if pref and pref.learned_weights:
            return pref.learned_weights
        return self.default_weights

    async def _get_weather(self, city: str) -> Dict:
        if not settings.OPENWEATHER_API_KEY or settings.OPENWEATHER_API_KEY == "demo_key":
            return {"temperature_c": 22.0, "condition": "Clear"}
        try:
            url = f"{settings.WEATHER_BASE_URL}/weather"
            params = {"q": city, "appid": settings.OPENWEATHER_API_KEY, "units": "metric"}
            async with httpx.AsyncClient(timeout=8) as client:
                r = await client.get(url, params=params)
            if r.status_code == 200:
                d = r.json()
                return {"temperature_c": d["main"]["temp"], "condition": d["weather"][0]["main"]}
        except Exception:
            pass
        return {"temperature_c": 22.0, "condition": "Clear"}

    async def _collaborative_score(self, db: AsyncSession, user_id: int, outfit_id: int) -> float:
        res = await db.execute(select(func.avg(Feedback.rating)).where(Feedback.outfit_id == outfit_id))
        avg = res.scalar()
        return float((avg or 3.0) / 5.0)

    async def recommend(self, db: AsyncSession, user_id: int, occasion: str = "casual", city: str = "New York", top_k: int = 5, seed_outfit_id: Optional[int] = None) -> List[Dict]:
        weights = await self._get_weights(db, user_id)
        weather = await self._get_weather(city)
        res = await db.execute(select(Outfit))
        outfits = res.scalars().all()
        if not outfits:
            return []
        seed_embedding = None
        seed_colors = None
        if seed_outfit_id is not None:
            seed = next((o for o in outfits if o.id == seed_outfit_id), None)
            if seed:
                seed_embedding = seed.embedding
                seed_colors = seed.dominant_colors
        scored = []
        for o in outfits:
            if seed_outfit_id is not None and o.id == seed_outfit_id:
                continue
            content = cosine(seed_embedding, o.embedding) if seed_embedding and o.embedding else 0.5
            collab = await self._collaborative_score(db, user_id, o.id)
            wscore = weather_score(weather, o.season or "all", o.tags or [])
            harmony = color_harmony_score(seed_colors or [], o.dominant_colors or []) if seed_colors else 0.5
            occ = 1.0 if (o.occasion or "").lower() == (occasion or "").lower() else 0.3
            score = (weights[0]*content + weights[1]*collab + weights[2]*wscore + weights[3]*harmony + weights[4]*occ)
            scored.append({"outfit_id": o.id, "filename": o.filename, "occasion": o.occasion, "score": round(float(score), 4), "components": {"content": round(content, 3), "collaborative": round(collab, 3), "weather": round(wscore, 3), "color_harmony": round(harmony, 3), "occasion": round(occ, 3)}})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
