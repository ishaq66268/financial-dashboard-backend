from fastapi import FastAPI, HTTPException
from utils import upsert_entry, delete_by_date, get_entries
from schemas import EntryIn, EntryOut
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Financial Dashboard API Running"}

@app.post("/entry", response_model=EntryOut)
async def create_entry(entry: EntryIn):
    """Create or update a financial entry"""
    try:
        return await upsert_entry(entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/entries", response_model=list[EntryOut])
async def list_entries():
    """List all entries"""
    try:
        return await get_entries({})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/entry/{entry_date}")
async def remove_entry(entry_date: str):
    """Delete entry by date (YYYY-MM-DD)"""
    try:
        date_obj = datetime.strptime(entry_date, "%Y-%m-%d").date()
        success = await delete_by_date(date_obj)
        return {"deleted": success}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
