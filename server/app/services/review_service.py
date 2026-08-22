from uuid import UUID

from app.database import repositories as repo


async def get_or_create_today_review(user_id: UUID):
    existing = await repo.get_today_review(user_id)
    if existing:
        return existing
    return await repo.create_daily_review(user_id)
    pass
