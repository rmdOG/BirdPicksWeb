from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

# This file defines the API endpoint for fetching schedule data.
router = APIRouter()

@router.get("/schedule/", response_model=List[schemas.RawSchedule], tags=["Schedule"])
def read_schedule(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    """
    Retrieves the NHL schedule from the database.
    
    You can use the 'skip' and 'limit' query parameters for pagination.
    For example: /schedule/?skip=10&limit=10
    """
    schedule_data = crud.get_schedule(db, skip=skip, limit=limit)
    return schedule_data
