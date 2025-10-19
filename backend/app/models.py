from sqlalchemy import Column, Integer, String, Date, Time
from .database import Base

class RawSchedule(Base):
    """
    SQLAlchemy model for the raw NHL schedule data.
    This file is the single source of truth for the 'raw_schedule' table's structure.
    The column names here ('visitor', 'home') are what the database will use.
    """
    __tablename__ = 'raw_schedule'

    id = Column(Integer, primary_key=True, index=True)
    
    # These columns must have a value, so nullable is False.
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    visitor = Column(String, nullable=False)
    home = Column(String, nullable=False)

    # These columns can be empty (e.g., before a game is played).
    visitor_goals = Column(Integer, nullable=True)
    home_goals = Column(Integer, nullable=True)
    attendance = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)

