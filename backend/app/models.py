from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from .database import Base

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    wins = Column(Integer)
    losses = Column(Integer)
    goals_for = Column(Integer)
    # Add more...

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))
    travel_distance = Column(Float)
    # Add outcome for training...

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"))
    goals = Column(Integer)
    # Add position, etc.