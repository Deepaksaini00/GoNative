from uuid import UUID

from .connection import database


# ----- Users -----------
async def get_user_by_id(user_id: UUID):
    return await database.fetch_one(
        "SELECT * FROM users WHERE id = :id", {"id": str(user_id)}
    )


async def get_user_by_email(email: str):
    return await database.fetch_one(
        "SELECT * FROM users WHERE email = :email", {"email": email}
    )


async def create_user(name: str, email: str, hashed_password: str):
    return await database.fetch_one(
        "INSERT INTO users (name, email, hashed_password) VALUES (:name, :email, :hashed_password)",
        {"name": name, "email": email, "hashed_password": hashed_password},
    )
