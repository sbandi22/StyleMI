"""
SQLAlchemy ORM models for StyleMI.
Tables: users, outfits, feedback, history, preferences.
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Boolean
)
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    outfits = relationship("Outfit", back_populates="owner")
    feedback = relationship("Feedback", back_populates="user")
    history = relationship("History", back_populates="user")
    preferences = relationship("Preference", back_populates="user", uselist=False)


class Outfit(Base):
    __tablename__ = "outfits"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String(255), nullable=False)
    image_path = Column(String(512), nullable=False)
    occasion = Column(String(64), index=True)
    season = Column(String(32), index=True)
    embedding = Column(JSON)
    dominant_colors = Column(JSON)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="outfits")
    feedback = relationship("Feedback", back_populates="outfit")


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    outfit_id = Column(Integer, ForeignKey("outfits.id"))
    rating = Column(Integer)
    liked = Column(Boolean, default=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedback")
    outfit = relationship("Outfit", back_populates="feedback")


class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recommended_ids = Column(JSON)
    context = Column(JSON)
    score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="history")


class Preference(Base):
    __tablename__ = "preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    favorite_colors = Column(JSON)
    favorite_styles = Column(JSON)
    avoid_tags = Column(JSON)
    learned_weights = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="preferences")
