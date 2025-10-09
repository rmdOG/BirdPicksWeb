# BirdPicksWeb
Web app for NHL game and player predictions.

## Setup
- **Backend**: `cd backend && source venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload`
- **Frontend**: `cd frontend && npm install && npm run dev`
- **DB**: PostgreSQL with `pg_birdpickweb`, user `postgres`, password `RyndvsTTG22`.

## Data
- Upload CSVs/Excel via frontend (`http://localhost:3000`) or backend (`/data/upload`).
- Supported tables: skaters, goalies, teams, games.