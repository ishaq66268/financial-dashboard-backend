from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional, Literal
from datetime import date as dtdate
from .schemas import EntryIn, EntryOut
from .utils import upsert_entry, delete_by_date, get_entries

app = FastAPI(title="Financial Dashboard API with MongoDB")

# ✅ Root endpoint
@app.get("/")
async def root():
    return {"message": "Financial Dashboard Backend is running 🚀"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/entries", response_model=EntryOut)
async def create_or_update_entry(payload: EntryIn):
    """Create or update an entry for a given date"""
    return await upsert_entry(payload)

@app.get("/entries", response_model=List[EntryOut])
async def list_entries(
    view: Literal["all","daily","monthly"]="all",
    date: Optional[dtdate]=None,
    month: Optional[int]=None,
    year: Optional[int]=None,
):
    """Fetch entries (all, daily, or monthly view)"""
    q = {}
    if view == "daily" and date:
        q = {"date": str(date)}
    elif view == "monthly" and month and year:
        q = {"date": {"$regex": f"^{year}-{month:02d}-"}}
    entries = await get_entries(q)
    return entries

@app.delete("/entries/{date}", status_code=204)
async def delete(date: dtdate):
    """Delete entry by date"""
    ok = await delete_by_date(date)
    if not ok:
        raise HTTPException(status_code=404, detail="No data for given date")
    return
