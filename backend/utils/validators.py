"""Input validation helpers."""
from fastapi import HTTPException

VALID_OCCASIONS = {"casual", "formal", "athletic", "evening", "business", "party"}
VALID_SEASONS = {"summer", "winter", "spring", "autumn", "all"}


def validate_occasion(occasion: str) -> None:
    if occasion.lower() not in VALID_OCCASIONS:
        raise HTTPException(400, f"Invalid occasion. Allowed: {sorted(VALID_OCCASIONS)}")


def validate_season(season: str) -> None:
    if season.lower() not in VALID_SEASONS:
        raise HTTPException(400, f"Invalid season. Allowed: {sorted(VALID_SEASONS)}")
