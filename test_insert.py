from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from datetime import date

MONGO_URL = "mongodb+srv://datauser123:userdata@cluster0.gfj0zmv.mongodb.net/financial_dashboard?retryWrites=true&w=majority&appName=Cluster0"

async def insert_test_entry():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client["financial_dashboard"]
    entries = db["entries"]

    test_doc = {
        "date": str(date.today()),
        "counter_amount": 1000,
        "material_cost": 400,
        "savings": 100
    }

    result = await entries.insert_one(test_doc)
    print("Inserted document ID:", result.inserted_id)

    # Fetch and print all documents
    all_docs = await entries.find().to_list(length=10)
    print("Current documents in 'entries' collection:")
    for doc in all_docs:
        print(doc)

asyncio.run(insert_test_entry())
