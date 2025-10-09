from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from .database import get_db
from .scrapers.nhl_scraper import scrape_nhl_data
from .ml.predictors import predict_player_streak
from .schemas import ScrapeRequest, GamePredict, PredictionResponse
import pandas as pd
from datetime import datetime

app = FastAPI(title="NHL Predictor API")

@app.get("/")
def read_root():
    return {"msg": "NHL Predictor Backend Ready"}

@app.post("/data/scrape")
def trigger_scrape(request: ScrapeRequest, db=Depends(get_db)):
    try:
        result = scrape_nhl_data(request.season, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/data/upload")
async def upload_csv(file: UploadFile = File(...), db=Depends(get_db)):
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(400, detail="Only CSV files allowed")
        df = pd.read_csv(file.file)
        for _, row in df.iterrows():
            game = Game(
                id=int(row['game_id']),
                date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                home_team_id=int(row['home_team_id']),
                away_team_id=int(row['away_team_id']),
                travel_distance=float(row.get('travel_distance', 0.0))
            )
            db.merge(game)
        db.commit()
        return {"status": "success", "records": len(df)}
    except Exception as e:
        db.rollback()
        raise HTTPException(400, detail=f"Upload failed: {str(e)}")

@app.get("/predict/player/{player_name}")
def predict_player(player_name: str, db=Depends(get_db)):
    try:
        result = predict_player_streak(db, player_name)
        return result
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@app.post("/predict/game", response_model=PredictionResponse)
def predict_game(game: GamePredict):
    return PredictionResponse(win_prob_home=0.65, total_goals_range=(4.5, 6.2))