from app.config import settings
from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorCollection,
                                 AsyncIOMotorDatabase)
from app.logger import logger

class MongoDB:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db: AsyncIOMotorDatabase = None
        self.dbname: str = ""
        self.jobs: AsyncIOMotorCollection = None


    def init(self):
        self.client = AsyncIOMotorClient(settings.mongodb_uri,
            maxPoolSize=1000,
            minPoolSize=100)
        self.db = self.client[settings.mongodb_dbname]
        self.dbname = settings.mongodb_dbname
        self.jobs = self.db[settings.mongodb_collections["jobs"]]
        logger.info("MongoDB started")
    
    def disconnect(self):
        self.client.close()
        logger.info("MongoDB closed")


mongodb = MongoDB()