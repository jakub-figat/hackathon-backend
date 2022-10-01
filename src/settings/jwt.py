from pydantic import (
    BaseSettings,
    Field,
)


class JWTSettings(BaseSettings):
    token_secret_key: str = Field(..., env="ACCESS_TOKEN_SECRET_KEY")
    token_expiration_time: int = Field(60 * 24, env="ACCESS_TOKEN_EXPIRATION_TIME")
    refresh_expiration_time: int = Field(60 * 24 * 30, env="REFRESH_TOKEN_EXPIRATION_TIME")
