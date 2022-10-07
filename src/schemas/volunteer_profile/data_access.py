import datetime as dt
from typing import Any
from uuid import UUID

from src.schemas.base import BaseModel
from src.schemas.service.data_access import VolunteerServiceSchema
from src.utils.schemas import BaseInputSchema


class VolunteerProfileInputSchema(BaseInputSchema):
    user_id: UUID
    location: tuple[float, float]
    area_size: float
    working_from: dt.time
    working_to: dt.time
    city: str

    def to_orm_kwargs(self) -> dict[str, Any]:
        return {
            "user_id": str(self.user_id),
            "location_x": self.location[0],
            "location_y": self.location[1],
            "city": self.city,
            "area_size": self.area_size,
            "working_from": self.working_from,
            "working_to": self.working_to,
        }


class VolunteerProfileSchema(BaseModel):
    id: UUID
    user_id: UUID
    location_x: float
    location_y: float
    area_size: float
    working_from: dt.time
    working_to: dt.time
    city: str
    services: list[VolunteerServiceSchema] = []
