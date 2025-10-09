from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from .database import Base
import enum

class Situation(enum.Enum):
    all = "all"
    five_on_five = "5on5"
    five_on_four = "5on4"
    four_on_five = "4on5"
    other = "other"

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    abbreviation = Column(String)
    wins = Column(Integer)
    losses = Column(Integer)
    goals_for = Column(Integer)
    goals_against = Column(Integer)

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))
    travel_distance = Column(Float)

class Skater(Base):
    __tablename__ = "skaters"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    player_id = Column(Integer, index=True)
    season = Column(Integer)
    name = Column(String)
    team = Column(String)
    position = Column(String)
    situation = Column(Enum(Situation))
    games_played = Column(Integer)
    icetime = Column(Float)
    shifts = Column(Integer)
    on_ice_xgoals_percentage = Column(Float)
    i_f_xgoals = Column(Float)
    i_f_goals = Column(Integer)
    i_f_shots_on_goal = Column(Integer)
    i_f_high_danger_xgoals = Column(Float)
    i_f_high_danger_goals = Column(Integer)

class Goalie(Base):
    __tablename__ = "goalies"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    player_id = Column(Integer, index=True)
    season = Column(Integer)
    name = Column(String)
    team = Column(String)
    games_played = Column(Integer)
    icetime = Column(Float)
    on_ice_a_xgoals = Column(Float)
    on_ice_a_goals = Column(Integer)
    i_f_saved_shots_on_goal = Column(Integer)