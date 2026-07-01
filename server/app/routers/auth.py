from fastapi import APIRouter

from app.database.schema import LoginRequest, RegisterRequest, SessionResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=SessionResponse)
async def register(request: RegisterRequest):
    res = await auth_service.register(
        name=request.name,
        email=request.email,
        password=request.password,
    )
    print("~~~~~~", res)
    return res


@router.post("/login", response_model=SessionResponse)
async def login(request: LoginRequest):
    return await auth_service.login(
        email=request.email,
        password=request.password,
    )
