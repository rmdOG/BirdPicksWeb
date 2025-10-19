from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import upload
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Create Tables ---
# This line checks for the existence of your tables and creates them
# if they don't already exist. It will NOT delete or alter existing tables.
# This is the safe way to manage your schema.
logger.info("Creating tables if they do not exist...")
Base.metadata.create_all(bind=engine)
logger.info("Table check complete.")


# --- Development Only Code: REMOVED ---
# The code to drop tables on every restart has been removed to prevent data loss.
# logger.info("Dropping all existing tables from the database (Development Mode)...")
# Base.metadata.drop_all(bind=engine)


# --- Initialize FastAPI App ---
# This is the main application object that Uvicorn looks for.
app = FastAPI(
    title="BirdPicks API",
    description="API for NHL data analysis and predictions.",
    version="1.0.0"
)

# --- CORS Middleware ---
# This allows your frontend (at http://localhost:3000) to communicate with this backend.
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Include Routers ---
app.include_router(upload.router)

# --- Root Endpoint ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the BirdPicks API"}

