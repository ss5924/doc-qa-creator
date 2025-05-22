from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import POSTGRESQL_DB_URL, MONGO_DB_URL
from motor.motor_asyncio import AsyncIOMotorClient

__engine = create_async_engine(POSTGRESQL_DB_URL, echo=False)
async_session = async_sessionmaker(__engine, expire_on_commit=False)

__mongo_client = AsyncIOMotorClient(MONGO_DB_URL)
__mongo_db = __mongo_client["arxiv"]
mongo_collection = __mongo_db["papers"]
