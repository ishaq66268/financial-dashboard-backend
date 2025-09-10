from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get("MONGO_URL")
async def test():
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        db = client["financial_dashboard"]
        collections = await db.list_collection_names()
        print("✅ Connected! Collections:", collections)
    except Exception as e:
        print("❌ Connection failed:", e)

asyncio.run(test())
