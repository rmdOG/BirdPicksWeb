from pydantic import BaseModel
from datetime import date
from typing import Optional

class GamePredict(BaseModel):
    home_team: str
    away_team: str
    date: Optional[date] = None

class PredictionResponse(BaseModel):
    win_prob_home: float
    total_goals_range: tuple[float, float]
    # Add player stuff...

class ScrapeRequest(BaseModel):
    season: str = "2024"