from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from app.database.connection import database
from app.database.migration import apply_migrations
from app.database.migration_to_apply import MIGRATIONS


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


@app.get("/")
def read_root():
    return "Gonative"


# if __name__ == "__main__":
#     main()

if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8006)
