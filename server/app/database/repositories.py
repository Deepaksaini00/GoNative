from datetime import date
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


# concept progress


async def get_concept_progress(user_id: UUID, concept_id: int):
    return await database.fetch_one(
        """
        SELECT * FROM user_concept_progress WHERE user_id = :user_id AND concept_id = :concept_id
        """,
        {"user_id": str(user_id), "concept_id": concept_id},
    )


async def get_all_concept_progress(user_id: UUID):
    return await database.fetch_all(
        """
        SELECT * FROM user_concept_progress WHERE user_id = :user_id
        """,
        {"user_id": str(user_id)},
    )


async def upsert_concept_progress(
    user_id: UUID, concept_id: int, is_correct: bool, score: float
):
    await database.execute(
        """
        INSERT INTO user_concept_progress (user_id, concept_id,attempts_total, correct_total, mastry_score,last_seen_at)
        VALUES (:user_id, :concept_id,1, :correct, :score, now())
        ON CONFLICT (user_id, concept_id) DO UPDATE SET
        attempt_total = user_concept_progress.attempts_total + 1,
        correct_total = user_concept_progress.correct_total + :correct,
        mastry_score = :score,
        last_seen_at = now()
        """,
        {
            "user_id": str(user_id),
            "concept_id": concept_id,
            "correct": 1 if is_correct else 0,
            "score": score,
        },
    )


# lesson Session
async def create_lesson_session(
    user_id: UUID,
    lesson_id: int,
    gemini_model: str,
    prompt_version: str,
):
    return await database.fetch_one(
        """
        INSERT INTO lesson_sessions (user_id, lesson_id, gemini_model, prompt_version)
        VALUES (:user_id, :lesson_id, :gemini_model, :prompt_version)
        RETURNING *
        """,
        {
            "user_id": str(user_id),
            "lesson_id": lesson_id,
            "gemini_model": gemini_model,
            "prompt_version": prompt_version,
        },
    )


# questions


async def create_question(
    session_id: UUID,
    concept_id: int,
    item_index: int,
    prompt_hi: str,
    correct_answer: str,
    question_type: str,
    metadata: dict | None = None,
):
    import json

    return await database.fetch_one(
        """
        INSERT INTO questions (session_id, concept_id, item_index, prompt_hi, correct_answer, question_type, metadata)
        VALUES (:session_id, :concept_id, :item_index, :prompt_hi, :correct_answer, :question_type, :metadata)
        RETURNING *
        """,
        {
            "session_id": str(session_id),
            "concept_id": concept_id,
            "item_index": item_index,
            "prompt_hi": prompt_hi,
            "correct_answer": correct_answer,
            "question_type": question_type,
            "metadata": json.dumps(metadata) if metadata else None,
        },
    )


async def get_question_by_id(question_id: UUID):
    return await database.fetch_one(
        "SELECT * FROM questions WHERE id = :id", {"id": str(question_id)}
    )


# user Answers
async def save_answer(
    user_id: UUID,
    question_id: UUID,
    answer: str,
    is_correct: bool,
    score: float,
    error_type: str | None = None,
    explanation_hi: str | None = None,
):
    return await database.fetch_one(
        """
        INSERT INTO user_answers (user_id, question_id, answer, is_correct, score, error_type, explanation_hi)
        VALUES (:user_id, :question_id, :answer, :is_correct, :score, :error_type, :explanation_hi)
        RETURNING *
        """,
        {
            "user_id": str(user_id),
            "question_id": str(question_id),
            "answer": answer,
            "is_correct": is_correct,
            "score": score,
            "error_type": error_type,
            "explanation_hi": explanation_hi,
        },
    )


async def get_recent_answers(user_id: UUID, concept_id: int, limit: int = 20):
    return await database.fetch_all(
        "SELECT * FROM user_answers ua JOIN questions q ON q.id =ua.question_id WHERE ua.user_id = :user_id AND q.concept_id = :concept_id ORDER BY ua.created_at DESC LIMIT :limit",
        {
            "user_id": str(user_id),
            "concept_id": concept_id,
            "limit": limit,
        },
    )


# Daily Review
async def get_today_review(
    user_id: UUID,
):
    return await database.fetch_one(
        """
    SELECT * FROM daily_reviews WHERE user_id = :user_id AND review_date = :today
    """,
    )
    {"user_id": str(user_id), "today": date.today()}
    pass


async def create_daily_review(
    user_id: UUID,
):
    return await database.fetch_one(
        """
        INSERT INTO daily_reviews (user_id, review_date)
        VALUES (:user_id, :today)
        RETURNING *
        """,
        {
            "user_id": str(user_id),
            "today": date.today(),
        },
    )


async def complete_daily_review(
    review_id: UUID,
):
    await database.execute(
        """
        UPDATE daily_reviews SET completed = true WHERE id = :id
        """,
        {
            "id": str(review_id),
        },
    )
