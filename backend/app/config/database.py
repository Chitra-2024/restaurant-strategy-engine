import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config.settings import get_settings

logger = logging.getLogger(__name__)

mongo_client: Optional[AsyncIOMotorClient] = None
database: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo() -> None:
    global mongo_client, database

    settings = get_settings()
    mongo_client = AsyncIOMotorClient(
        settings.mongodb_uri,
        serverSelectionTimeoutMS=2000,
        connectTimeoutMS=2000,
    )
    database = mongo_client[settings.mongodb_db_name]

    try:
        await mongo_client.admin.command("ping")
    except Exception as error:
        logger.warning("MongoDB ping failed during startup: %s", error)


async def disconnect_from_mongo() -> None:
    global mongo_client, database

    if mongo_client is not None:
        mongo_client.close()

    mongo_client = None
    database = None


def get_database() -> AsyncIOMotorDatabase:
    if database is None:
        raise RuntimeError("MongoDB database is not initialized.")

    return database
