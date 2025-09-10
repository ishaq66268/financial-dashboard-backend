from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_URL)
db = client["financial_dashboard"]
entries_collection = db["entries"]
