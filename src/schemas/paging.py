from typing import (
    Generic,
    TypeVar,
)

from pydantic.fields import Field

from src.schemas.base import BaseModel
from src.settings import settings


ResponseSchema = TypeVar("ResponseSchema", bound=BaseModel)


class PagingInputParams(BaseModel):
    page_number: int = Field(default=1, gt=0)

    def to_limit_offset(self, page_size: int = settings.page_size) -> tuple[int, int]:
        return settings.page_size + 1, (self.page_number - 1) * page_size


class PaginatedResponseSchema(Generic[ResponseSchema], BaseModel):
    count: int
    page_number: int
    has_next_page: bool
    results: list[ResponseSchema]

    @classmethod
    def from_results(cls, results: list[ResponseSchema], page_number: int) -> "PaginatedResponseSchema":
        return cls(
            count=len(results[:-1]),
            page_number=page_number,
            has_next_page=len(results) > settings.page_size,
            results=results[:-1],
        )
