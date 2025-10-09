from app.database import Base, engine
from app.models import RawPlayerSeason, RawGoalies, RawTeams, RawLinesPairings, RawPlayerGame, RawGameLevel, RawShotData, RawPlayerInfo, RawSchedule, TeamsLookup

Base.metadata.create_all(bind=engine)
print("Tables created successfully.")