import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# --- Load Environment Variables ---
# This line loads the variables from your .env file (e.g., DATABASE_URL)
# into the environment, making them accessible to your application.
load_dotenv()

# --- Database Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL")

# Add a check to ensure the DATABASE_URL was loaded correctly
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Please create a .env file with your database connection string.")

# --- SQLAlchemy Engine Setup ---
# The engine is the entry point to the database.
engine = create_engine(DATABASE_URL)

# --- SessionLocal ---
# Each instance of SessionLocal will be a new database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Base ---
# We will inherit from this class to create each of the ORM models.
Base = declarative_base()

# --- Database Dependency ---
# This function will be used in our API endpoints to get a database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

