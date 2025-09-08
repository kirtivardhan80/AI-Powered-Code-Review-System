import os
import asyncio
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

async def test_connection():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    try:
        await client.admin.command("ping")
        print("✅ MongoDB connection successful!")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)

asyncio.run(test_connection())
