from uuid import UUID

from src.schemas.base import BaseModel


class VolunteerServiceSchema(BaseModel):
    id: UUID
    name: str
