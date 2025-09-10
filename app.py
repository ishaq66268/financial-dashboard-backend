from fastapi import FastAPI
from utils import upsert_entry, delete_by_date, get_entries
from schemas import EntryIn, EntryOut

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Financial Dashboard API Running"}

# Example endpoints
@app.post("/entry")
async def create_entry(entry: EntryIn):
    return await upsert_entry(entry)

@app.get("/entries")
async def list_entries():
    return await get_entries({})

@app.delete("/entry/{entry_date}")
async def remove_entry(entry_date: str):
    from datetime import datetime
    date_obj = datetime.strptime(entry_date, "%Y-%m-%d").date()
    success = await delete_by_date(date_obj)
    return {"deleted": success}
