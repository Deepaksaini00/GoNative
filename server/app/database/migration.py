from datetime import datetime
from typing import Callable, Coroutine

from databases import Database

MIGRATION_TABLE_NAME = "migration_version"
MigrationFunctions = Callable[[Database], Coroutine]


async def apply_migrations(db: Database, migrations: list[MigrationFunctions]) -> None:
    # print("migrations", [m.__name__ for m in migrations], len(migrations))

    async with db.transaction():
        migration_table = await db.fetch_one(
            """
            SELECT table_name FROM information_schema.tables WHERE table_name = :table_name
            """,
            {"table_name": MIGRATION_TABLE_NAME},
        )
        if migration_table is None:
            await db.execute(
                """
                CREATE TABLE migration_version (
                    version INTEGER PRIMARY KEY,
                    applied_on TEXT NOT NULL
                )
                """
            )

        migrations_applied = await db.fetch_one(
            " SELECT count(*) as count FROM migration_version"
        )
        assert migrations_applied is not None

        count: int = migrations_applied["count"]

        # print(
        #     f"-------------------- count: {count} and len(migrations): {len(migrations)}"
        # )

        if count > len(migrations):
            raise Exception(
                "Database has newer migrations than your code. Please deploy a newer version."
            )

        for i, migration in enumerate(migrations[count:]):
            await migration(db)
            await db.execute(
                "INSERT INTO migration_version (version, applied_on) VALUES (:version, :applied_on)",
                {"version": count + i + 1, "applied_on": datetime.now().isoformat()},
            )
