from src.settings.aws import AWSSettings
from src.settings.db import DatabaseSettings
from src.settings.general import GeneralSettings
from src.settings.jwt import JWTSettings
from src.settings.paging import PagingSettings


class Settings(GeneralSettings, DatabaseSettings, JWTSettings, PagingSettings, AWSSettings):
    ...


settings = Settings()
