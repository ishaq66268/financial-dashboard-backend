from .database import entries_collection
from .schemas import EntryIn
from datetime import date as dtdate

async def upsert_entry(payload: EntryIn):
    profit = payload.counter_amount - payload.material_cost - payload.savings
    doc = payload.model_dump()
    doc["profit"] = profit
    doc["date"] = str(payload.date)
    await entries_collection.update_one(
        {"date": doc["date"]}, {"$set": doc}, upsert=True
    )
    return doc

async def delete_by_date(d: dtdate):
    res = await entries_collection.delete_one({"date": str(d)})
    return res.deleted_count > 0

async def get_entries(filter_query: dict = {}):
    cursor = entries_collection.find(filter_query).sort("date", 1)
    results = []
    async for doc in cursor:
        results.append(doc)
    return results
