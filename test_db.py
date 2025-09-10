from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

MONGO_URL = "mongodb+srv://datauser123:userdata@cluster0.gfj0zmv.mongodb.net/financial_dashboard?retryWrites=true&w=majority&appName=Cluster0"

async def test_connection():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client["financial_dashboard"]
    print("✅ Connected to:", db.name)
    # Try inserting a test document
    result = await db.test_collection.insert_one({"msg": "Hello Atlas"})
    print("Inserted ID:", result.inserted_id)

asyncio.run(test_connection())
