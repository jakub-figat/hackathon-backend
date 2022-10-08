import datetime as dt
from typing import (
    Any,
    Type,
)
from uuid import UUID

import pydantic
from pydantic.class_validators import validator

from src.schemas.base import BaseModel
from src.schemas.service.dto import VolunteerServiceSchema
from src.schemas.ticket import data_access


class TicketInputSchema(BaseModel):
    title: str
    location: tuple[float, float]
    city: str
    description: str
    valid_until: dt.datetime
    services_ids: list[UUID]


class TicketQueryParams(pydantic.BaseModel):
    area_size: float = 0
    valid_from: dt.datetime | None = None
    valid_to: dt.datetime | None = None
    city: str | None = None
    user_id: UUID | None = None

    @validator("valid_to")
    def validate_valid_to(cls, valid_to: dt.time, values: dict[str, Any]) -> dt.time:
        if (valid_from := values.get("valid_from")) is not None and valid_to is not None:
            if valid_from >= valid_to:
                raise ValueError("Invalid time range")

        return valid_to


class TicketFilterParams(BaseModel):
    area_size: float = 0
    location: tuple[float, float] | None = None
    valid_from: dt.time | None = None
    valid_to: dt.time | None = None
    city: str | None = None
    user_id: UUID | None = None
    services_ids: list[UUID]


class TicketSchema(BaseModel):
    id: UUID
    title: str
    user_id: UUID
    location: tuple[float, float]
    city: str
    description: str
    valid_until: dt.datetime
    services: list[VolunteerServiceSchema] = []

    @classmethod
    def from_orm(cls: Type["TicketSchema"], obj: Any, **kwargs) -> "TicketSchema":
        ticket = data_access.TicketSchema.from_orm(obj)

        return cls(
            **ticket.dict(exclude={"location_x", "location_y"}),
            location=(ticket.location_x, ticket.location_y),
            **kwargs,
        )
