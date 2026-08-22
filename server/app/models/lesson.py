from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.progress import UserProgress


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    title_hindi: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    level: Mapped[int] = mapped_column(Integer, default=1)  # 1=beginner, 2=elementary, 3=intermediate
    order_index: Mapped[int] = mapped_column(Integer, default=0)  # order within level
    category: Mapped[str] = mapped_column(String, default="general")  # greetings, numbers, grammar, etc.
    content: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # structured lesson content from Gemini
    is_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    progresses: Mapped[list[UserProgress]] = relationship(
        "UserProgress", back_populates="lesson"
    )
    quiz_questions: Mapped[list[QuizQuestion]] = relationship(
        "QuizQuestion", back_populates="lesson", cascade="all, delete-orphan"
    )


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lessons.id"), nullable=False
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_hindi: Mapped[str | None] = mapped_column(Text, nullable=True)
    question_type: Mapped[str] = mapped_column(String, default="mcq")  # mcq, fill_blank, translate
    options: Mapped[list | None] = mapped_column(JSON, nullable=True)  # list of option strings
    correct_answer: Mapped[str] = mapped_column(String, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    explanation_hindi: Mapped[str | None] = mapped_column(Text, nullable=True)

    lesson: Mapped[Lesson] = relationship("Lesson", back_populates="quiz_questions")