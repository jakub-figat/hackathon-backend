from pydantic.env_settings import BaseSettings
from pydantic.fields import Field


class GeneralSettings(BaseSettings):
    domain: str = "http://localhost:8000"
    allowed_hosts: list[str] = ["http://localhost:3000"]
    debug: bool = Field(True, env="DEBUG")
