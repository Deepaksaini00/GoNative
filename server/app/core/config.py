from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    SECRET_KEY: str = ""
    DATABASE_URL: str = ""
    TEST_DB_URL: str = ""
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=".env")

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]


settings = Settings()
