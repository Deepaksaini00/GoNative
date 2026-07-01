from uuid import UUID

from fastapi import HTTPException, status

from app.database import repositories as repo


async def get_all_lessons_with_status(user_id: UUID):
    lessons = await repo.get_all_lessons()
    result = []
    for lesson in lessons:
        progress = await repo.get_lesson_progress(user_id, lesson["id"])
        result.append(
            {
                "id": lesson["id"],
                "code": lesson["code"],
                "title_hi": lesson["title_hi"],
                "title_en": lesson["title_en"],
                "level": lesson["level"],
                "progress": progress,
                "position": lesson["position"],
                "status": lesson["status"] if progress else "locked",
                "mastery_score": float(progress["mastery_score"] if progress else 0.0),
            }
        )
    return result


async def get_lesson_details(user_id: UUID, lesson_id: int):
    lesson = await repo.get_lesson_by_id(lesson_id)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found"
        )
    concepts = await repo.get_lesson_concepts(lesson_id)
    concept_list = []
    for c in concepts:
        progress = await repo.get_concept_progress(user_id, c["id"])
        concept_list.append(
            {
                "id": c["id"],
                "code": c["code"],
                "title_hi": c["title_hi"],
                "title_en": c["title_en"],
                "difficulty": c["difficulty"],
                "mastery_score": float(progress["mastery_score"] if progress else 0.0),
            }
        )

    return {
        "id": lesson["id"],
        "title_hi": lesson["title_hi"],
        "title_en": lesson["title_en"],
        "concepts": concept_list,
    }
