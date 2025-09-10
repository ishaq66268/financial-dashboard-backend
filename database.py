from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "financial_dashboard")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
entries_collection = db["entries"]

# function to return DB instance
def get_db():
    return db
