import os
import motor.motor_asyncio
from dotenv import load_dotenv
import asyncio

# ✅ Load environment variables
load_dotenv()

# ✅ Get Mongo URI and DB Name from environment
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")  # Optional, if not included in URI

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI is missing in your .env file")

# ✅ Create MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

# ✅ Select database (from URI or DB_NAME)
if DB_NAME:
    db = client[DB_NAME]
else:
    db = client.get_default_database()  # Will work if URI has DB name

if db is None:
    raise ValueError("❌ Database is not selected. Add DB_NAME in .env or include in URI")

# ✅ Collections
reviews_collection = db["reviews"]

# ✅ Test Connection
async def test_connection():
    try:
        print("🔍 Testing MongoDB connection...")
        await client.admin.command("ping")
        print("✅ MongoDB connection successful!")
        print(f"✅ Using database: {db.name}")
        print(f"✅ Reviews collection ready: {reviews_collection.name}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
