"""User and preferences endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional

from database.db import get_db
from database.models import User, Preference

router = APIRouter()


class UserIn(BaseModel):
    username: str
    email: Optional[str] = None


class PreferenceIn(BaseModel):
    user_id: int
    favorite_colors: List[str] = []
    favorite_styles: List[str] = []
    avoid_tags: List[str] = []


@router.post("/")
async def create_user(payload: UserIn, db: AsyncSession = Depends(get_db)):
    user = User(username=payload.username, email=payload.email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"id": user.id, "username": user.username}


@router.post("/preferences")
async def save_preferences(payload: PreferenceIn, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Preference).where(Preference.user_id == payload.user_id))
    pref = res.scalar_one_or_none()
    if pref is None:
        pref = Preference(user_id=payload.user_id)
        db.add(pref)
    pref.favorite_colors = payload.favorite_colors
    pref.favorite_styles = payload.favorite_styles
    pref.avoid_tags = payload.avoid_tags
    await db.commit()
    return {"status": "ok"}


@router.get("/preferences/{user_id}")
async def get_preferences(user_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Preference).where(Preference.user_id == user_id))
    pref = res.scalar_one_or_none()
    if not pref:
        raise HTTPException(404, "No preferences for user")
    return {
        "favorite_colors": pref.favorite_colors,
        "favorite_styles": pref.favorite_styles,
        "avoid_tags": pref.avoid_tags,
        "learned_weights": pref.learned_weights,
    }
