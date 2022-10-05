import datetime as dt
from typing import Any
from uuid import UUID

from pydantic.class_validators import validator

from src.schemas.base import BaseModel
from src.schemas.service.dto import VolunteerServiceSchema


class VolunteerProfileInputSchema(BaseModel):
    location: tuple[float, float]
    area_size: float
    working_from: dt.time
    working_to: dt.time
    city: str
    services_ids: list[UUID]

    @validator("working_to")
    def validate_working_to(cls, working_to: dt.time, values: dict[str, Any]) -> dt.time:
        if values["working_from"] >= working_to:
            raise ValueError("Invalid time range")

        return working_to


class VolunteerProfileSchema(BaseModel):
    id: UUID
    user_id: UUID
    location: tuple[float, float]
    area_size: float
    working_from: dt.datetime
    working_to: dt.datetime
    city: str
    services: list[VolunteerServiceSchema]
