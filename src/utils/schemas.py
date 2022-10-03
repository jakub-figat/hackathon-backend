from abc import (
    ABC,
    abstractmethod,
)
from typing import Any

from pydantic import BaseModel


class BaseInputSchema(BaseModel, ABC):
    @abstractmethod
    def to_orm_kwargs(self) -> dict[str, Any]:
        pass


def to_camel_case(field_name: str) -> str:
    words = field_name.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])
