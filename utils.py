from datetime import datetime, date
from database import entries_collection
from schemas import EntryIn, EntryOut

def doc_to_entryout(doc) -> EntryOut:
    """Convert MongoDB doc into EntryOut"""
    # Convert date string to datetime.date
    doc_date = doc["date"]
    if isinstance(doc_date, str):
        doc_date = datetime.strptime(doc_date, "%Y-%m-%d").date()

    return EntryOut(
        id=str(doc["_id"]),
        date=doc_date,
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
    # Store date as string in MongoDB
    doc["date"] = str(payload.date)

    result = await entries_collection.find_one_and_update(
        {"date": doc["date"]},
        {"$set": doc},
        upsert=True,
        return_document=True
    )

    if not result:
        result = await entries_collection.find_one({"date": doc["date"]})

    return doc_to_entryout(result)

async def get_entries(query: dict = None) -> list[EntryOut]:
    """Fetch entries with optional filters"""
    query = query or {}
    cursor = entries_collection.find(query).sort("date", 1)
    docs = await cursor.to_list(length=None)
    return [doc_to_entryout(doc) for doc in docs]

async def delete_by_date(entry_date: date) -> bool:
    """Delete entry by date"""
    # Convert date to string to match MongoDB document
    date_str = entry_date.strftime("%Y-%m-%d")
    result = await entries_collection.delete_one({"date": date_str})
    return result.deleted_count > 0
