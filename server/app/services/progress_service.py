from uuid import UUID
from app.database import repositories as repo

async def get_user_progress(user_id: UUID) -> :
    concepts_prog = await repo.get_all_concept_progress(user_id)
    return[
        {
            "concept_id": p["concept_id"],
            "attempts_total": p["attempts_total"],
            "correct_total": p["correct_total"],
            "mastery_score": float (p["mastery_score"]),
            "last_seen_at": p["last_seen_at"],
        }
        for p in concepts_prog
    ]
