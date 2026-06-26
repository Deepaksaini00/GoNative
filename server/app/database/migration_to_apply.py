from databases import Database

from app.database.migration import MigrationFunctions


async def m001_initial_tables(db: Database) -> None:
    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            hashed_password TEXT NOT NULL,
            native_lang TEXT DEFAULT 'hi',
            target_lang TEXT DEFAULT 'en',
            created_at TIMESTAMP NOT NULL DEFAULT now()
        );
        """
    )

    await db.execute("""
        CREATE TABLE IF NOT EXISTS concepts (
            id              SERIAL PRIMARY KEY,
            code            TEXT UNIQUE NOT NULL,
            title_en        TEXT NOT NULL,
            title_hi        TEXT NOT NULL,
            description_en  TEXT,
            description_hi  TEXT,
            difficulty      INT NOT NULL DEFAULT 1,
            parent_id       INT REFERENCES concepts(id) ON DELETE SET NULL
        )
    """)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS lessons (
            id              SERIAL PRIMARY KEY,
            code            TEXT UNIQUE NOT NULL,
            title_en        TEXT NOT NULL,
            title_hi        TEXT NOT NULL,
            level           INT NOT NULL,
            position        INT NOT NULL,
            created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS lesson_concepts (
            lesson_id       INT REFERENCES lessons(id) ON DELETE CASCADE,
            concept_id      INT REFERENCES concepts(id) ON DELETE CASCADE,
            position        INT NOT NULL,
            PRIMARY KEY (lesson_id, concept_id)
        )
    """)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS user_concept_progress (
            user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
            concept_id      INT REFERENCES concepts(id) ON DELETE CASCADE,
            attempts_total  INT NOT NULL DEFAULT 0,
            correct_total   INT NOT NULL DEFAULT 0,
            streak_correct  INT NOT NULL DEFAULT 0,
            mastery_score   NUMERIC(5,2) NOT NULL DEFAULT 0.0,
            last_seen_at    TIMESTAMPTZ,
            mastered_at     TIMESTAMPTZ,
            PRIMARY KEY (user_id, concept_id)
        )
    """)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS user_lesson_progress (
            user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
            lesson_id       INT REFERENCES lessons(id) ON DELETE CASCADE,
            status          TEXT NOT NULL DEFAULT 'locked',
            mastery_score   NUMERIC(5,2) NOT NULL DEFAULT 0.0,
            started_at      TIMESTAMPTZ,
            completed_at    TIMESTAMPTZ,
            PRIMARY KEY (user_id, lesson_id)
        )
    """)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS lesson_sessions (
            id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
            lesson_id       INT REFERENCES lessons(id) ON DELETE SET NULL,
            generated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
            gemini_model    TEXT NOT NULL,
            prompt_version  TEXT NOT NULL,
            metadata        JSONB
        )
    """)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            session_id      UUID REFERENCES lesson_sessions(id) ON DELETE CASCADE,
            concept_id      INT REFERENCES concepts(id) ON DELETE SET NULL,
            item_index      INT NOT NULL,
            prompt_hi       TEXT NOT NULL,
            correct_answer  TEXT NOT NULL,
            question_type   TEXT NOT NULL,
            metadata        JSONB
        )
    """)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS user_answers (
            id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
            question_id     UUID REFERENCES questions(id) ON DELETE CASCADE,
            user_answer     TEXT NOT NULL,
            is_correct      BOOLEAN NOT NULL,
            score           NUMERIC(5,2) NOT NULL,
            error_type      TEXT,
            explanation_hi  TEXT,
            evaluated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS daily_reviews (
            id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
            review_date     DATE NOT NULL,
            completed       BOOLEAN NOT NULL DEFAULT FALSE,
            created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
            UNIQUE (user_id, review_date)
        )
    """)


# Future migrations added here as new functions:
# async def m002_update_user(db: Database) -> None:
#     await db.execute("""
#         ALTER TABLE users ADD COLUMN username TEXT
#     """)


MIGRATIONS: list[MigrationFunctions] = [
    m001_initial_tables,
    m001_initial_tables,
]
