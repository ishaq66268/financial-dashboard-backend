from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional, Literal
from datetime import date as dtdate
from schemas import EntryIn, EntryOut
from utils import upsert_entry, delete_by_date, get_entries

app = FastAPI(title="Financial Dashboard API with MongoDB")

# ✅ Root endpoint
@app.get("/")
async def root():
    return {"message": "Financial Dashboard Backend is running 🚀"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# ✅ Create / Update entry
@app.post("/entries", response_model=EntryOut)
async def create_or_update_entry(payload: EntryIn):
    result = await upsert_entry(payload.dict())
    if not result:
        raise HTTPException(status_code=400, detail="Insert/Update failed")
    return result

# ✅ Fetch entries (all / daily / monthly)
@app.get("/entries", response_model=List[EntryOut])
async def list_entries(
    view: Literal["all", "daily", "monthly"] = "all",
    date: Optional[dtdate] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
):
    if view == "daily" and date:
        entries = await get_entries(str(date))
    elif view == "monthly" and month and year:
        start = f"{year}-{month:02d}-01"
        end = f"{year}-{month:02d}-31"
        entries = await get_entries(start, end)
    else:
        entries = await get_entries()
    return entries

# ✅ Delete by date
@app.delete("/entries/{date}", status_code=204)
async def delete(date: dtdate):
    deleted_count = await delete_by_date(str(date))
    if not deleted_count:
        raise HTTPException(status_code=404, detail="No data for given date")
    return
