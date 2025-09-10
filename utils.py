from datetime import date
from backend.database import entries_collection
from backend.schemas import EntryIn, EntryOut

def doc_to_entryout(doc) -> EntryOut:
    """Convert MongoDB doc into EntryOut"""
    return EntryOut(
        id=str(doc["_id"]),
        date=doc["date"],
        counter_amount=doc["counter_amount"],
        material_cost=doc["material_cost"],
        savings=doc["savings"],
        profit=doc["counter_amount"] - doc["material_cost"] - doc["savings"],
    )

async def upsert_entry(payload: EntryIn) -> EntryOut:
    """Insert or update entry for given date"""
    profit = payload.counter_amount - payload.material_cost - payload.savings
    doc = payload.dict()
    doc["profit"] = profit

    result = await entries_collection.find_one_and_update(
        {"date": str(payload.date)},
        {"$set": doc},
        upsert=True,
        return_document=True
    )

    # if Mongo doesn't return doc on upsert, fetch it manually
    if not result:
        result = await entries_collection.find_one({"date": str(payload.date)})

    return doc_to_entryout(result)

async def get_entries(query: dict) -> list[EntryOut]:
    """Fetch entries with optional filters"""
    cursor = entries_collection.find(query).sort("date", 1)
    docs = await cursor.to_list(length=None)
    return [doc_to_entryout(doc) for doc in docs]

async def delete_by_date(entry_date: date) -> bool:
    """Delete entry by date"""
    result = await entries_collection.delete_one({"date": str(entry_date)})
    return result.deleted_count > 0
