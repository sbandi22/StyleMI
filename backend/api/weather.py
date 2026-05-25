"""Weather API integration (OpenWeatherMap)."""
from fastapi import APIRouter, HTTPException
import httpx
from config import settings

router = APIRouter()


@router.get("/{city}")
async def get_weather(city: str):
    """Fetch current weather for a city. Falls back to a stub if no API key configured."""
    if not settings.OPENWEATHER_API_KEY or settings.OPENWEATHER_API_KEY == "demo_key":
        return {
            "city": city,
            "temperature_c": 22.0,
            "condition": "Clear",
            "humidity": 50,
            "wind_kph": 8.0,
            "source": "stub",
        }
    url = f"{settings.WEATHER_BASE_URL}/weather"
    params = {"q": city, "appid": settings.OPENWEATHER_API_KEY, "units": "metric"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params)
    if r.status_code != 200:
        raise HTTPException(r.status_code, f"Weather API error: {r.text}")
    data = r.json()
    return {
        "city": city,
        "temperature_c": data["main"]["temp"],
        "condition": data["weather"][0]["main"],
        "humidity": data["main"]["humidity"],
        "wind_kph": data["wind"]["speed"] * 3.6,
        "source": "openweathermap",
    }
