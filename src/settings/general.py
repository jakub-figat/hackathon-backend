from pydantic.env_settings import BaseSettings


class GeneralSettings(BaseSettings):
    allowed_hosts: list[str] = ["http://localhost:3000"]
