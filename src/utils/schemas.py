from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class BaseInputSchema(BaseModel, ABC):
    @abstractmethod
    def to_orm_kwargs(self) -> dict[str, Any]:
        pass
