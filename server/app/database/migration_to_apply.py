from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from app.database.migration import MigrationFunction


async def m001_initial_tables(conn: AsyncConnection) -> None:
    await conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS users (
                id              UUID PRIMARY KEY,
                name            TEXT NOT NULL,
                email           TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL,
                native_lang     TEXT NOT NULL DEFAULT 'hi',
                target_lang     TEXT NOT NULL DEFAULT 'en',
                created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
                last_login      TIMESTAMPTZ,
                current_streak  INTEGER DEFAULT 0,
                total_xp        INTEGER DEFAULT 0
            )
            """
        )
    )

    await conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS lessons (
                id            SERIAL PRIMARY KEY,
                title         TEXT NOT NULL,
                title_hindi   TEXT,
                description   TEXT,
                level         INTEGER DEFAULT 1,
                order_index   INTEGER DEFAULT 0,
                category      TEXT DEFAULT 'general',
                content       JSONB,
                is_generated  BOOLEAN DEFAULT false,
                created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """
        )
    )

    await conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS quiz_questions (
                id                SERIAL PRIMARY KEY,
                lesson_id         INTEGER NOT NULL REFERENCES lessons(id),
                question_text     TEXT NOT NULL,
                question_hindi    TEXT,
                question_type     TEXT DEFAULT 'mcq',
                options           JSONB,
                correct_answer    TEXT NOT NULL,
                explanation       TEXT,
                explanation_hindi TEXT
            )
            """
        )
    )

    await conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS user_progress (
                id             SERIAL PRIMARY KEY,
                user_id        UUID NOT NULL REFERENCES users(id),
                lesson_id      INTEGER NOT NULL REFERENCES lessons(id),
                status         TEXT DEFAULT 'not_started',
                score          FLOAT DEFAULT 0.0,
                attempts       INTEGER DEFAULT 0,
                last_attempted TIMESTAMPTZ,
                completed_at   TIMESTAMPTZ,
                xp_earned      INTEGER DEFAULT 0
            )
            """
        )
    )

    await conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id                  SERIAL PRIMARY KEY,
                user_id             UUID NOT NULL REFERENCES users(id),
                lesson_id           INTEGER NOT NULL REFERENCES lessons(id),
                attempt_type        TEXT DEFAULT 'lesson',
                answers             JSONB,
                score               FLOAT DEFAULT 0.0,
                total_questions     INTEGER DEFAULT 0,
                correct_answers     INTEGER DEFAULT 0,
                time_taken_seconds  INTEGER DEFAULT 0,
                ai_feedback         TEXT,
                created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """
        )
    )


# Future migrations added here as new functions:
# async def m002_add_user_field(conn: AsyncConnection) -> None:
#     await conn.execute(text("ALTER TABLE users ADD COLUMN username TEXT"))


MIGRATIONS: list[MigrationFunction] = [
    m001_initial_tables,
]