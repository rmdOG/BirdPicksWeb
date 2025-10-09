from fastapi import FastAPI
from .database import get_db
from .routes.upload import router as upload_router

app = FastAPI(title="NHL Predictor API")

app.include_router(upload_router)

@app.get("/")
def read_root():
    return {"msg": "NHL Predictor Backend Ready"}