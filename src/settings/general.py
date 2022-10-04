from pydantic.env_settings import BaseSettings


class GeneralSettings(BaseSettings):
    allowed_hosts: list[str] = ["*"]
