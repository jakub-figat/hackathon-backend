from src.settings.db import DatabaseSettings
from src.settings.jwt import JWTSettings


class Settings(DatabaseSettings, JWTSettings):
    ...


settings = Settings()
