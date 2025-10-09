from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from .database import get_db
import pandas as pd
import io
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

app = FastAPI(title="NHL Predictor API")

# Updated NHL arenas with Utah Hockey Club (replacing Arizona Coyotes)
nhl_arenas = {
    'Anaheim Ducks': (33.807895, -117.876447),
    'Utah Hockey Club': (40.7683, -111.9017),  # Delta Center, Salt Lake City
    'Boston Bruins': (42.366386, -71.061616),
    'Buffalo Sabres': (42.874835, -78.876223),
    'Calgary Flames': (51.037387, -114.052001),
    'Detroit Red Wings': (42.324958, -83.052084),
    'Edmonton Oilers': (53.546562, -113.496529),
    'Florida Panthers': (26.158400, -80.325319),
    'Los Angeles Kings': (34.043094, -118.267062),
    'Montreal Canadiens': (45.496470, -73.569945),  # Corrected spelling
    'San Jose Sharks': (37.332670, -121.901351),
    'Ottawa Senators': (45.296754, -75.927115),
    'Vancouver Canucks': (49.277604, -123.109633),
    'Tampa Bay Lightning': (27.942742, -82.451793),
    'Las Vegas Golden Knights': (36.102908, -115.178132),
    'Toronto Maple Leafs': (43.643540, -79.379028),
    'Chicago Blackhawks': (41.880098, -87.674442),
    'Carolina Hurricanes': (35.802913, -78.722331),
    'Colorado Avalanche': (39.748721, -105.007682),
    'Columbus Blue Jackets': (39.969368, -83.006205),
    'Dallas Stars': (32.790525, -96.810715),
    'New Jersey Devils': (40.733012, -74.172097),
    'Minnesota Wild': (44.944139, -93.100850),
    'New York Islanders': (40.682617, -73.975331),
    'Nashville Predators': (36.159033, -86.778682),
    'New York Rangers': (40.750523, -73.993420),
    'St. Louis Blues': (38.626435, -90.202611),
    'Philadelphia Flyers': (39.901674, -75.171888),
    'Winnipeg Jets': (49.892724, -97.143712),
    'Pittsburgh Penguins': (40.439481, -79.989581),
    'Washington Capitals': (38.898144, -77.020923)
}

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

@app.get("/")
def read_root():
    return {"msg": "NHL Predictor Backend Ready"}

@app.post("/data/upload")
async def upload_file(file: UploadFile = File(...), table: str = "skaters", db=Depends(get_db)):
    try:
        contents = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(contents), engine='openpyxl')
        else:
            raise HTTPException(400, detail="Only CSV or XLSX allowed")

        if table == "skaters":
            columns = ['player_id', 'season', 'name', 'team', 'position', 'situation', 'games_played', 'icetime', 'shifts', 'on_ice_xgoals_percentage', 'i_f_xgoals', 'i_f_goals', 'i_f_shots_on_goal', 'i_f_high_danger_xgoals', 'i_f_high_danger_goals']
            df = df.rename(columns={
                'playerId': 'player_id',
                'season': 'season',
                'name': 'name',
                'team': 'team',
                'position': 'position',
                'situation': 'situation',
                'games_played': 'games_played',
                'icetime': 'icetime',
                'shifts': 'shifts',
                'onIce_xGoalsPercentage': 'on_ice_xgoals_percentage',
                'I_F_xGoals': 'i_f_xgoals',
                'I_F_goals': 'i_f_goals',
                'I_F_shotsOnGoal': 'i_f_shots_on_goal',
                'I_F_highDangerxGoals': 'i_f_high_danger_xgoals',
                'I_F_highDangerGoals': 'i_f_high_danger_goals'
            })
        elif table == "goalies":
            columns = ['player_id', 'season', 'name', 'team', 'games_played', 'icetime', 'on_ice_a_xgoals', 'on_ice_a_goals', 'i_f_saved_shots_on_goal']
            df = df.rename(columns={
                'playerId': 'player_id',
                'season': 'season',
                'name': 'name',
                'team': 'team',
                'games_played': 'games_played',
                'icetime': 'icetime',
                'OnIce_A_xGoals': 'on_ice_a_xgoals',
                'OnIce_A_goals': 'on_ice_a_goals',
                'I_F_savedShotsOnGoal': 'i_f_saved_shots_on_goal'
            })
        elif table == "teams":
            columns = ['season', 'name', 'abbreviation', 'wins', 'losses', 'goals_for', 'goals_against']
            df = df.rename(columns={
                'team': 'name',
                'teamAbbreviation': 'abbreviation'
            })
        elif table == "games":
            columns = ['date', 'home_team_id', 'away_team_id', 'travel_distance']
            # Map team names to a simpler key (abbreviation or name) for ARENAS lookup
            df['home_team_id'] = df['home_team_id'].map(lambda x: next((k for k, v in nhl_arenas.items() if x in k), x))
            df['away_team_id'] = df['away_team_id'].map(lambda x: next((k for k, v in nhl_arenas.items() if x in k), x))
            df['date'] = pd.to_datetime(df['date']).dt.date
            df['travel_distance'] = df.apply(
                lambda row: haversine_distance(
                    nhl_arenas.get(row['home_team_id'], (0, 0))[0],
                    nhl_arenas.get(row['home_team_id'], (0, 0))[1],
                    nhl_arenas.get(row['away_team_id'], (0, 0))[0],
                    nhl_arenas.get(row['away_team_id'], (0, 0))[1]
                ) if row['home_team_id'] in nhl_arenas and row['away_team_id'] in nhl_arenas else 0.0,
                axis=1
            )
            df = df.rename(columns={'home_team': 'home_team_id', 'away_team': 'away_team_id'})
        else:
            raise HTTPException(400, detail=f"Unsupported table: {table}")

        df = df[[col for col in df.columns if col in columns]]
        df.to_sql(table, db.bind, if_exists='append', index=False)
        return {"status": "success", "records": len(df)}
    except Exception as e:
        db.rollback()
        raise HTTPException(400, detail=f"Upload failed: {str(e)}")