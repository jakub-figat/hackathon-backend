from src.settings.db import DatabaseSettings
from src.settings.general import GeneralSettings
from src.settings.jwt import JWTSettings


class Settings(GeneralSettings, DatabaseSettings, JWTSettings):
    ...


settings = Settings()
