from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import upload, schedule  # Ensure 'schedule' is imported here
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Create Tables ---
logger.info("Creating tables if they do not exist...")
Base.metadata.create_all(bind=engine)
logger.info("Table check complete.")

# --- Initialize FastAPI App ---
app = FastAPI(
    title="BirdPicks API",
    description="API for NHL data analysis and predictions.",
    version="1.0.0"
)

# --- CORS Middleware ---
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
# Both the upload and the new schedule router must be included.
app.include_router(upload.router)
app.include_router(schedule.router)

# --- Root Endpoint ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the BirdPicks API"}

