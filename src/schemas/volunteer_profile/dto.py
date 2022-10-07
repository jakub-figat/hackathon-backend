import datetime as dt
from typing import Any
from uuid import (
    UUID,
    uuid4,
)

from fastapi import Query
from pydantic.class_validators import validator
from pydantic.fields import Field

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
        if (working_from := values.get("working_from")) is not None and working_to is not None:
            if working_from >= working_to:
                raise ValueError("Invalid time range")

        return working_to


class VolunteerProfileQueryParams(BaseModel):
    area_size: float = 0
    working_from: dt.time | None = None
    working_to: dt.time | None = None
    city: str | None = None

    @validator("working_to")
    def validate_working_to(cls, working_to: dt.time, values: dict[str, Any]) -> dt.time:
        if (working_from := values.get("working_from")) is not None and working_to is not None:
            if working_from >= working_to:
                raise ValueError("Invalid time range")

        return working_to


class VolunteerProfileFilterParams(BaseModel):
    location: tuple[float, float] | None = None
    area_size: float = 0
    working_from: dt.time | None = None
    working_to: dt.time | None = None
    city: str | None = None
    services_ids: list[UUID] = []


class VolunteerProfileSchema(BaseModel):
    id: UUID
    user_id: UUID
    location: tuple[float, float]
    area_size: float
    working_from: dt.time
    working_to: dt.time
    city: str
    services: list[VolunteerServiceSchema]
