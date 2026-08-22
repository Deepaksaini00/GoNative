from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.services import review_service

router = APIRouter(prefix="/review", tags=["review"])


@router.get("/daily")
async def daily_review(user_id: UUID = Depends(get_current_user)):
    return await review_service.get_or_create_today_review(user_id)
