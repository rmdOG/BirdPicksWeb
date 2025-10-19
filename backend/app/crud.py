from sqlalchemy.orm import Session
from . import models

# This file contains the functions that interact directly with the database.
# 'CRUD' stands for Create, Read, Update, Delete.

def get_schedule(db: Session, skip: int = 0, limit: int = 1000):
    """
    Retrieves a list of schedule entries from the database,
    ordered by date and time. Supports pagination.
    """
    return db.query(models.RawSchedule).order_by(models.RawSchedule.date, models.RawSchedule.time).offset(skip).limit(limit).all()
