from pydantic import (
    BaseSettings,
    Field,
)


class AWSSettings(BaseSettings):
    bucket_name: str = Field(..., env="BUCKET_NAME")
