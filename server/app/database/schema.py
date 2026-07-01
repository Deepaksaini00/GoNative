from datetime import datetime
from uuid import UUID

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


# UserLogut


class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    native_lang: str
    target_lang: str
    created_at: datetime


# --- Lesson ---
class LessonOut(BaseModel):
    id: int
    code: str
    title_en: str
    title_hi: str
    level: int
    position: int


# --- Concept ---
class ConceptOut(BaseModel):
    id: int
    code: str
    title_en: str
    title_hi: str
    difficulty: int


# --- Answer submission ---
class SubmitAnswerRequest(BaseModel):
    question_id: UUID
    session_id: UUID
    user_answer: str


class SubmitAnswerResponse(BaseModel):
    is_correct: bool
    score: float
    error_type: str | None
    explanation_hi: str | None


# --- Progress ---
class ConceptProgressOut(BaseModel):
    concept_id: int
    attempts_total: int
    correct_total: int
    mastery_score: float
    status: str | None
    last_seen_at: datetime | None


class LessonProgressOut(BaseModel):
    lesson_id: int
    status: str
    mastery_score: float
    started_at: datetime | None
    completed_at: datetime | None


# --- Daily Review ---


class DailyReviewOut(BaseModel):
    id: UUID
    review_date: str
    completed: bool
