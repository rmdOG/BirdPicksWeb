from pydantic import BaseModel
from typing import Optional
import datetime

# This file defines the "shape" of the data when it's sent to or from the API.
# It ensures that the data is valid and has the correct types.

class RawSchedule(BaseModel):
    id: int
    date: datetime.date
    time: datetime.time
    visitor: str
    home: str
    visitor_goals: Optional[int] = None
    home_goals: Optional[int] = None
    attendance: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        # This allows the Pydantic model to be created directly from
        # a SQLAlchemy ORM (database) object.
        from_attributes = True
