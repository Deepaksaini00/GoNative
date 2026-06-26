import asyncio
from app.database.connection import database

async def test():
    await database.connect()
    result = await database.fetch_one("SELECT version()")
    print("Connected!  PostgreSQL version", result)
    await database.disconnect()


asyncio.run(test())

