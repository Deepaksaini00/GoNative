from uuid import UUID

from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.database import repositories as repo

# register a new user


async def register(name: str, email: str, password: str):
    existing = await repo.get_user_by_email(email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed = hash_password(password)
    print("#####", len(hashed))
    user = await repo.create_user(name=name, email=email, hashed_password=hashed)
    token = create_access_token(UUID(str(user["id"])))
    print(f"token: {token}, len: {len(token)}, user: {user}")
    return {"access_token": token, "token_type": "bearer"}


# Login a User


async def login(email: str, password: str):
    user = await repo.get_user_by_email(email)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token(user["id"])
    return {"access_token": token, "token_type": "bearer"}
