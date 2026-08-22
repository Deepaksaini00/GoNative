from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.services import progress_service

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/")
async def get_progress(user_id: UUID = Depends(get_current_user)):
    return await progress_service.get_user_progress(user_id)
