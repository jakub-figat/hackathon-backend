from uuid import UUID

from pydantic.fields import Field

from src.schemas.base import BaseModel


class ReviewInputSchema(BaseModel):
    volunteer_profile_id: UUID
    rating: int = Field(..., ge=1, le=5)
    text: str = Field(..., max_length=100)
