# Financial Dashboard API (FastAPI + MongoDB)

## Local setup
```bash
cd backend
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export MONGO_URL="mongodb://localhost:27017"
uvicorn app:app --reload
```

## Deploy (Render example)
- Use Dockerfile provided.
- Set environment variable `MONGO_URL` to your MongoDB Atlas connection string.
