"""
Weather -> outfit compatibility scoring.
Heuristics based on temperature, condition, and outfit season/tags.
"""
from typing import Dict


def weather_score(weather: Dict, outfit_season: str, outfit_tags: list) -> float:
    temp = weather.get("temperature_c", 20.0)
    cond = (weather.get("condition") or "").lower()
    tags = [t.lower() for t in (outfit_tags or [])]

    if temp >= 25:
        ideal = {"summer", "all"}
    elif temp >= 15:
        ideal = {"spring", "autumn", "all"}
    elif temp >= 5:
        ideal = {"autumn", "winter", "all"}
    else:
        ideal = {"winter", "all"}

    s = 1.0 if (outfit_season or "all").lower() in ideal else 0.4

    if "rain" in cond and "waterproof" in tags:
        s += 0.2
    if "snow" in cond and "winter" in tags:
        s += 0.2
    if "clear" in cond and "summer" in tags:
        s += 0.1
    return max(0.0, min(s, 1.0))
