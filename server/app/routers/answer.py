from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.database.schema import SubmitAnswerRequest, SubmitAnswerResponse
from app.services import answer_service

router = APIRouter(prefix="/answers", tags=["answers"])


@router.post(
    "/submit",
    response_model=SubmitAnswerResponse,
)
async def submit_answer(
    body: SubmitAnswerRequest, user_id: UUID = Depends(get_current_user)
):
    return await answer_service.answer_process(
        user_id=user_id,
        question_id=body.question_id,
        user_answer=body.user_answer,
    )
