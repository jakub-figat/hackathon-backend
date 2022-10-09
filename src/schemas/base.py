from pydantic import BaseModel as PydanticBaseModel

from src.utils.schemas import to_camel_case


class BaseModel(PydanticBaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel_case
        allow_population_by_field_name = True
