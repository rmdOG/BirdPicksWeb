from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import get_db
from .routes.upload import router as upload_router

app = FastAPI(title="NHL Predictor API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(upload_router)

@app.get("/")
def read_root():
    return {"msg": "NHL Predictor Backend Ready"}