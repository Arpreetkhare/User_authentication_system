from app.models.user_models import User
from motor.motor_asyncio import AsyncIOMotorClient
from app.helper.user_helper import logger

async def get_user_by_username(db: AsyncIOMotorClient, username: str):
    
    user = await db["users"].find_one({"username": username}) 
    logger.debug(f"Looking for user: {username} in database")
    return user

async def create_user(db: AsyncIOMotorClient, new_user: dict):
    logger.debug(f"Creating new user: {new_user}")
    return await db.users.insert_one(new_user)
