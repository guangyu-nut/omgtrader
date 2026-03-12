from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "omgtrader-backend"
    database_url: str = "sqlite:///./omgtrader.db"

    model_config = SettingsConfigDict(env_prefix="OMGTRADER_", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
