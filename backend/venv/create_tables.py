from app.database import Base, engine
from app.models import Team, Game, Skater, Goalie  # Import all models

Base.metadata.create_all(bind=engine)
print("Tables created successfully.")