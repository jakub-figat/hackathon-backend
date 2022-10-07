from pydantic.env_settings import BaseSettings


class PagingSettings(BaseSettings):
    page_size: int = 50
