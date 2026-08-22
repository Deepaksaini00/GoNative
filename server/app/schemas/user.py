from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    native_language: str = "hindi"
    target_language: str = "english"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    name: str
    email: str
    native_language: str = Field(
        validation_alias=AliasChoices("native_language", "native_lang")
    )
    target_language: str = Field(
        validation_alias=AliasChoices("target_language", "target_lang")
    )
    current_streak: int = 0
    total_xp: int = 0
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class UserUpdate(BaseModel):
    name: Optional[str] = None
    native_language: Optional[str] = None
    target_language: Optional[str] = None