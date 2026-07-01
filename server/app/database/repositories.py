from uuid import UUID

from .connection import database


# ----- Users -----------
async def get_user_by_id(user_id: UUID):
    return await database.fetch_one(
        "SELECT * FROM users WHERE id = :id", {"id": str(user_id)}
    )


async def get_user_by_email(email: str):
    return await database.fetch_one(
        "SELECT * FROM users WHERE email = :email", {"email": email}
    )


async def create_user(name: str, email: str, hashed_password: str):
    return await database.fetch_one(
        "INSERT INTO users (name, email, hashed_password) VALUES (:name, :email, :hashed_password)",
        {"name": name, "email": email, "hashed_password": hashed_password},
    )


# concepts --------
#
async def get_all_concepts():
    return await database.fetch_all("SELECT * FROM concepts ORDER BY difficulty")


async def get_concept_by_id(concept_id: UUID):
    return await database.fetch_one(
        "SELECT * FROM concepts WHERE id = :id", {"id": concept_id}
    )


async def get_concepts_by_code(code: str):
    return await database.fetch_all(
        "SELECT * FROM concepts WHERE code = :code", {"code": code}
    )


async def get_concept_progress(user_id: UUID, concept_id: int):

    return await database.fetch_one(
        """
        SELECT * FROM user_concept_progress WHERE user_id = :user_id AND concept_id = :concept_id
        """,
        {"user_id": user_id, "concept_id": concept_id},
    )


# lessons --------


async def get_all_lessons():
    return await database.fetch_all("SELECT * FROM lessons ORDER BY level, position")


async def get_lesson_by_id(lesson_id: int):
    return await database.fetch_one(
        "SELECT * FROM lessons WHERE id = :id", {"id": lesson_id}
    )


async def get_lesson_concepts(lesson_id: int):
    return await database.fetch_all(
        """
        SELECT c.* FROM concepts c JOIN lesson_concepts lc ON lc.concept_id = c.id WHERE lc.lesson_id = :lesson_id ORDER BY lc.position
        """,
        {"lesson_id": lesson_id},
    )


# lesson progress -------


async def get_lesson_progress(user_id: UUID, lesson_id: int):
    return await database.fetch_one(
        """
        SELECT * FROM user_lesson_progress WHERE user_id = :user_id AND lesson_id = :lesson_id
        """,
        {"user_id": user_id, "lesson_id": lesson_id},
    )


async def upsert_lesson_progress(
    user_id: UUID, lesson_id: int, status: str, mastery_score: float
):
    await database.execute(
        """
        INSERT INTO user_lesson_progress (user_id, lesson_id, status, mastery_score, started_at, completed_at) VALUES (:user_id, :lesson_id, :status, :mastery_score, :now())
        ON CONFLICT (user_id, lesson_id) DO UPDATE SET
        status = :status, mastery_score = :score,  CASE WHEN :status = 'mastered' THEN now() ELSE NULL END
        """,
        {
            "user_id": str(user_id),
            "lesson_id": lesson_id,
            "status": status,
            "score": mastery_score,
        },
    )
