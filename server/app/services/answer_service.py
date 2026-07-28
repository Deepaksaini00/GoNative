from uuid import UUID

from fastapi import HTTPException, status

from app.ai.evaluator import evaluate_answer
from app.database import repositories as repo


async def answer_process(user_id: UUID, question_id: UUID, user_answer: str) -> dict:
    question = await repo.get_question_by_id(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )

    ai_result = await evaluate_answer(
        question_text=question["prompt_hi"],
        correct_answer=question["answer"],
        user_answer=user_answer,
    )
    await repo.save_answer(
        user_id=user_id,
        question_id=question_id,
        answer=user_answer,
        is_correct=ai_result["is_correct"],
        score=ai_result["score"],
        error_type=ai_result.get("error_type"),
        explanation_hi=ai_result.get("explanation_hi"),
    )
    await repo.upsert_concept_progress(
        user_id=user_id,
        concept_id=question["concept_id"],
        is_correct=ai_result["is_correct"],
        score=ai_result["score"],
    )
    return {
        "is_correct": ai_result["is_correct"],
        "score": ai_result["score"],
        "error_type": ai_result.get("error_type"),
        "explanation_hi": ai_result.get("explanation_hi"),
    }
