import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from ml.similarity import cosine
from ml.color_analyzer import color_harmony_score
from ml.weather_scorer import weather_score


def test_cosine_identity():
    v = [1.0, 0.0, 0.0]
    assert abs(cosine(v, v) - 1.0) < 1e-6


def test_color_harmony_range():
    s = color_harmony_score([(255, 0, 0)], [(0, 255, 255)])
    assert 0.0 <= s <= 1.0


def test_weather_score_warm_summer():
    s = weather_score({"temperature_c": 28, "condition": "Clear"}, "summer", ["summer"])
    assert s > 0.8
