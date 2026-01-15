from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, SecretStr


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: int

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
