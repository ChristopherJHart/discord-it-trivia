"""Contains bot settings."""

from pydantic import BaseSettings, FilePath


class Settings(BaseSettings):
    """Schema for bot settings."""

    QUESTION_POOL_FILEPATH: FilePath = "models/question_pool.yaml"
    DEBUG: bool = False
    DISCORD_TOKEN: str = None
    TEST_GUILD: int = None

    class Config:
        """Pydantic BaseSettings object configuration.

        Prioritizes a .env file first, and falls back to the environment.
        """

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
