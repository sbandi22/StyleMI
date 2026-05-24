<div align="center">

# StyleMI — Fashion Recommendation Engine

**AI-powered outfit recommendations based on occasion, weather, color matching, and personal style**

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.14-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## Overview

StyleMI is a production-ready fashion recommendation engine that combines computer vision, natural language understanding, and ensemble machine learning to deliver personalised outfit suggestions. It integrates real-time weather data, user preference learning, and visual similarity scoring to recommend contextually appropriate outfits.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        StyleMI Architecture                      │
├───────────────┬─────────────────────────┬───────────────────────┤
│  Frontend     │       Backend           │    ML Pipeline        │
│  (Streamlit)  │      (FastAPI)          │                       │
│               │                         │  ┌─────────────────┐  │
│  Dashboard    │  /api/recommend         │  │  CLIP Embeddings│  │
│  Upload UI    │  /api/upload            │  │  (outfit visual  │  │
│  History      │  /api/feedback          │  │   similarity)    │  │
│  Analytics    │  /api/weather           │  └────────┬────────┘  │
│               │  /api/preferences       │           │            │
│               │                         │  ┌────────▼────────┐  │
│               │  ┌──────────────────┐   │  │ Ensemble Model  │  │
│               │  │   SQLite DB      │   │  │ (CF + Content + │  │
│               │  │  - users         │   │  │  Weather score) │  │
│               │  │  - outfits       │   │  └────────┬────────┘  │
│               │  │  - feedback      │   │           │            │
│               │  │  - history       │   │  ┌────────▼────────┐  │
│               │  └──────────────────┘   │  │  Ranking &      │  │
│               │                         │  │  Scoring Layer  │  │
└───────────────┴─────────────────────────┴──┴─────────────────┴──┘
                          │                          │
              ┌───────────┴──────────┐   ┌──────────┴────────┐
              │   Weather API        │   │  OpenWeatherMap    │
              │   (OpenWeatherMap)   │   │  Free Tier        │
              └──────────────────────┘   └───────────────────┘
```

---

## Features

- **Visual Outfit Analysis** — CLIP embeddings extract semantic features from uploaded outfit images
- **Weather-Aware Recommendations** — integrates live weather data to suggest season/temperature appropriate outfits
- **Occasion Filtering** — casual, formal, athletic, evening, business filters
- **Color Harmony Scoring** — OpenCV-based palette extraction with complementary color matching
- **Ensemble ML Model** — combines collaborative filtering, content-based, and rule-based signals
- **User Preference Learning** — implicit feedback loop improves recommendations over time
- **Outfit Similarity Scoring** — cosine similarity on CLIP embeddings
- **Streamlit Dashboard** — interactive UI with upload, history, analytics
- **Beta Test Simulation** — 50-user simulation with accuracy metrics
- **Docker Support** — single `docker-compose up` deployment

---

## Project Structure

```
StyleMI/
├── backend/
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Configuration and environment variables
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py            # SQLAlchemy ORM models
│   │   └── db.py                # Database connection and session
│   ├── api/
│   │   ├── __init__.py
│   │   ├── recommendations.py   # Recommendation endpoints
│   │   ├── outfits.py           # Outfit CRUD endpoints
│   │   ├── users.py             # User and preferences endpoints
│   │   ├── weather.py           # Weather API integration
│   │   └── feedback.py          # Feedback collection endpoints
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── clip_encoder.py      # CLIP embedding extraction
│   │   ├── color_analyzer.py    # OpenCV color palette analysis
│   │   ├── recommender.py       # Ensemble recommendation engine
│   │   ├── similarity.py        # Cosine similarity scoring
│   │   ├── weather_scorer.py    # Weather compatibility scoring
│   │   └── preference_learner.py # User preference model
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── image_processor.py   # Image preprocessing utilities
│   │   └── validators.py        # Input validation helpers
│   └── uploads/                 # Uploaded outfit images (gitignored)
├── frontend/
│   └── app.py                   # Streamlit dashboard
├── ml_pipeline/
│   ├── train.py                 # Model training pipeline
│   ├── evaluate.py              # Evaluation metrics and visualisation
│   ├── beta_simulation.py       # 50-user beta test simulation
│   └── feature_engineering.py  # Feature engineering pipeline
├── data/
│   ├── generate_dataset.py      # Sample dataset generator
│   ├── preprocess.py            # Data preprocessing scripts
│   └── sample/                  # Sample data files
├── tests/
│   ├── test_api.py
│   ├── test_ml.py
│   └── test_utils.py
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- pip or conda
- Docker (optional)

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/sbandi22/StyleMI.git
cd StyleMI

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your OpenWeatherMap API key

# 5. Generate sample dataset
python data/generate_dataset.py

# 6. Run the backend
cd backend
uvicorn main:app --reload --port 8000

# 7. Run the frontend (new terminal)
cd frontend
streamlit run app.py --server.port 8501
```

### Docker Setup

```bash
# Build and start all services
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/outfits/upload` | Upload outfit image |
| GET | `/api/outfits/{id}` | Get outfit details |
| POST | `/api/recommend` | Get recommendations |
| GET | `/api/weather/{city}` | Get weather data |
| POST | `/api/users/preferences` | Save user preferences |
| POST | `/api/feedback` | Submit outfit feedback |
| GET | `/api/history/{user_id}` | Get recommendation history |

Full interactive docs at `http://localhost:8000/docs` (Swagger UI)

---

## ML Pipeline

### Recommendation Engine

The ensemble model combines three signals with learned weights:

```
Final Score = w1 * ContentScore
            + w2 * CollaborativeScore
            + w3 * WeatherScore
            + w4 * ColorHarmonyScore
            + w5 * OccasionScore

Default weights: [0.30, 0.25, 0.20, 0.15, 0.10]
Weights adapt per user via preference learning
```

### CLIP Embeddings

Outfit images are encoded into 512-dimensional vectors using OpenAI CLIP (`ViT-B/32`). Similarity is computed via cosine distance on the embedding space.

### Color Analysis

OpenCV K-Means clustering extracts dominant color palettes (k=5). Color harmony scoring uses HSV wheel distance to evaluate complementary, analogous, and triadic combinations.

---

## Beta Test Results

Simulated across 50 synthetic users with varied preferences:

| Metric | Score |
|--------|-------|
| Precision@5 | 0.74 |
| Recall@10 | 0.68 |
| NDCG@10 | 0.71 |
| Click-through Rate | 38.2% |
| User Satisfaction (avg) | 4.1 / 5.0 |
| Cold-start Performance | 0.61 |

---

## Environment Variables

```env
# .env.example
OPENWEATHER_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./stylemi.db
SECRET_KEY=your-secret-key-here
CLIP_MODEL=ViT-B/32
MAX_UPLOAD_SIZE_MB=10
RECOMMENDATION_LIMIT=20
```

---

## Deployment

### Render / Railway

```bash
# Set environment variables in platform dashboard
# Backend: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
# Frontend: streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
```

### AWS EC2

```bash
# Install Docker on EC2
sudo apt update && sudo apt install docker.io docker-compose -y
git clone https://github.com/sbandi22/StyleMI.git
cd StyleMI
cp .env.example .env && nano .env  # add your keys
docker-compose up -d
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI 0.104 |
| ML Framework | TensorFlow 2.14, Scikit-learn |
| Vision | OpenAI CLIP (ViT-B/32), OpenCV |
| Frontend | Streamlit 1.28 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Image Processing | OpenCV, Pillow |
| Data | Pandas, NumPy |
| Visualisation | Plotly, Matplotlib |
| Containerisation | Docker, Docker Compose |

---

## License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">
Built by <a href="https://github.com/sbandi22">Sushma Bandi</a>
</div>
