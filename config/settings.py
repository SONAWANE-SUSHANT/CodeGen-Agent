from functools import lru_cache

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    express_api_base_url: AnyHttpUrl = Field(alias="EXPRESS_API_BASE_URL")
    gemini_api_key: str = Field(alias="GEMINI_API_KEY")
    qdrant_url: AnyHttpUrl = Field(alias="QDRANT_URL")
    app_env: str = Field(default="development", alias="APP_ENV")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def cors_origins(self) -> list[str]:
        if self.app_env == "production":
            return [str(self.express_api_base_url).rstrip("/")]

        return ["*"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
