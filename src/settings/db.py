from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    postgres_host: str = Field(..., env="POSTGRES_HOST")
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    postgres_database: str = Field(..., env="POSTGRES_DATABASE")
    postgres_port: int = Field(..., env="POSTGRES_PORT", default=5432)

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_database}"
        )
