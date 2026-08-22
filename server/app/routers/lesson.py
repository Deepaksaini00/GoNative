from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.services import lesson_service

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("/")
async def list_lessons(
    user_id: UUID = Depends(get_current_user),
):
    return await lesson_service.get_all_lessons_with_status(user_id)


@router.get("/{lesson_id}")
async def lesson_details(
    lesson_id: int,
    user_id: UUID = Depends(get_current_user),
):
    return await lesson_service.get_lesson_details(user_id, lesson_id)
