import databases
import pytest

from app.core.config import settings
from app.database import migration


@pytest.mark.asyncio
async def test_():
    db = databases.Database(settings.TEST_DB_URL)
    await db.connect()

    await db.execute("DROP TABLE IF EXISTS test_users")
    await db.execute("DROP TABLE IF EXISTS migration_version")

    print("```````````````````````````")

    async def migration_001(db: databases.Database):
        await db.execute("""
            CREATE TABLE test_users (
                id SERIAL PRIMARY KEY,
                email TEXT NOT NULL
            )
        """)

    # Apply migrations version 001

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    await migration.apply_migrations(db, [migration_001])
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    row = await db.fetch_one(" SELECT count(*) as count FROM migration_version")
    print("======================", row)
    assert row is not None
    assert row["count"] == 1

    row = await db.fetch_one(
        "SELECT table_name FROM information_schema.tables"
        " WHERE table_name = 'test_users'"
    )
    assert row is not None

    # Apply migrations version 1 again

    await migration.apply_migrations(db, [migration_001])

    row = await db.fetch_one(" SELECT count(*) as count FROM migration_version")
    assert row is not None
    assert row["count"] == 1

    print("*********** Migration version 001 applied")

    # Apply migrations version 002

    async def migration_002(db: databases.Database):
        await db.execute("""
            ALTER TABLE test_users ADD COLUMN name TEXT;
        """)

    print("Called migration 01 and 02 ")
    await migration.apply_migrations(db, [migration_001, migration_002])
    row = await db.fetch_one("SELECT count(*) as count FROM migration_version")
    assert row is not None

    print("row row row ------: ", row.count)

    assert row["count"] == 2

    print("*********** Migration version 002 applied")

    row = await db.fetch_one(
        """
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'test_users' AND column_name = 'name'
        """
    )
    assert row is not None

    with pytest.raises(Exception):
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        await migration.apply_migrations(db, [migration_001])

    await db.disconnect()
