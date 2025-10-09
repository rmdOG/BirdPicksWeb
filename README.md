## Quick Setup
- Backend: `cd backend && source venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload`
- Frontend: `cd frontend && npm install && npm run dev`
- DB: Ensure PostgreSQL is running with db `pg_birdpickweb`, user `nhl_user`, password `password`.