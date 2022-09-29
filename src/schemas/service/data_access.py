from typing import Any
from uuid import UUID

from src.schemas.base import BaseModel
from src.utils.schemas import BaseInputSchema


class VolunteerServiceInputSchema(BaseInputSchema):
    name: str

    def to_orm_kwargs(self) -> dict[str, Any]:
        return {"name": self.name}


class VolunteerServiceSchema(BaseModel):
    id: UUID
    name: str
