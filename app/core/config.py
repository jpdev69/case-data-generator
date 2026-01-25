from functools import lru_cache
from typing import Optional

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="Financial Support VA Case Simulator")
    environment: str = Field(default="local")
    api_prefix: str = Field(default="/api")
    debug: bool = Field(default=True)

    db_url: Optional[AnyUrl] = Field(default=None, description="Postgres connection URL")
    redis_url: str = Field(default="redis://redis:6379/0")

    s3_bucket: str = Field(default="case-simulator-dev")
    s3_endpoint_url: Optional[AnyUrl] = None
    s3_region: str = Field(default="us-east-1")

    llm_model: str = Field(default="gpt-4.1")
    llm_max_tokens: int = Field(default=2000)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
