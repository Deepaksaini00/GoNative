from pydantic import BaseModel, EmailStr


# Auth
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SessionResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
