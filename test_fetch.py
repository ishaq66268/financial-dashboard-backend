from database import entries_collection
import asyncio

async def fetch_entries():
    docs = await entries_collection.find({}).to_list(length=100)
    print("Documents:", docs)

asyncio.run(fetch_entries())
