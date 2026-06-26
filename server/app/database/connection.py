from databases import Database

from app.core.config import settings

database = Database(settings.DATABASE_URL)
# metadata = MetaData()


# async def connect_db():
#     await database.connect()


# async def diconnect_db():
#     await database.disconnect()
