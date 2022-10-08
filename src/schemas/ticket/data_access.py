import datetime as dt
from typing import Any
from uuid import UUID

from src.schemas.base import BaseModel
from src.schemas.service.data_access import VolunteerServiceSchema
from src.utils.schemas import BaseInputSchema


class TicketInputSchema(BaseInputSchema):
    location: tuple[float, float]
    city: str
    description: str
    valid_until: dt.datetime
    user_id: UUID

    def to_orm_kwargs(self) -> dict[str, Any]:
        return {
            "location_x": self.location[0],
            "location_y": self.location[1],
            "city": self.city,
            "description": self.description,
            "valid_until": self.valid_until,
            "user_id": str(self.user_id),
        }


class TicketSchema(BaseModel):
    id: UUID
    location_x: float
    location_y: float
    city: str
    description: str
    valid_until: dt.datetime
    user_id: UUID
    services: list[VolunteerServiceSchema] = []
