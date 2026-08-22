from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from app.database.connection import database
from app.database.migration import apply_migrations
from app.database.migration_to_apply import MIGRATIONS
from app.routers import answer, auth, lesson, progress, review


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await database.connect()
    await apply_migrations(database, MIGRATIONS)
    print("Database connected and migrations applied")
    yield

    # shutdown
    await database.disconnect()
    print("Database disconnected")


# app = FastAPI(title="GoNative API", version="1.0.0", lifespan=lifespan)

app = FastAPI(lifespan=lifespan, debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/api")
app.include_router(answer.router, prefix="/api")
app.include_router(lesson.router, prefix="/api")
app.include_router(progress.router, prefix="/api")
app.include_router(review.router, prefix="/api")


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8006)
