import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()




# Get MongoDB credentials from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")




# Connect to MongoDB using the credentials from .env
client = AsyncIOMotorClient(DATABASE_URL)
db = client["taskdb"]

def get_db():
    return db


