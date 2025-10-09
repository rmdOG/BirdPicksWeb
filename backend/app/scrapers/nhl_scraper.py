import hockey_scraper as hs
import pandas as pd
from sqlalchemy.orm import Session
from ..models import Game, Team
from datetime import datetime

def scrape_nhl_data(season: str, db: Session):
    try:
        # Scrape PBP and shifts for a season (e.g., "2024" = 2024-25)
        data = hs.scrape_seasons([int(season)], if_scrape_shifts=True, data_format='Pandas', docs_dir=True)
        if not data:
            return {"status": "error", "message": "No data scraped"}

        all_games = pd.concat([game['pbp'] for game in data if 'pbp' in game], ignore_index=True)
        all_shifts = pd.concat([game['shifts'] for game in data if 'shifts' in game], ignore_index=True)

        # Example: Insert games (simplified; assumes team IDs exist)
        for _, row in all_games.iterrows():
            game = Game(
                id=int(row['game_id']),
                date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                home_team_id=int(row.get('home_team_id', 0)),  # Adjust field names per version
                away_team_id=int(row.get('away_team_id', 0)),
                travel_distance=500.0  # Placeholder; compute later
            )
            db.merge(game)  # Avoid duplicates
        db.commit()

        # Save shifts to DB (add table in models.py later)
        all_shifts.to_sql('shifts', db.bind, if_exists='append', index=False)

        return {"status": "success", "records": len(all_games), "shifts": len(all_shifts)}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}