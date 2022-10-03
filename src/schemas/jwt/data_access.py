from typing import Any
from uuid import UUID

from src.schemas.base import BaseModel
from src.utils.schemas import BaseInputSchema


class RefreshTokenInputSchema(BaseInputSchema):
    user_id: UUID
    jti: UUID

    def to_orm_kwargs(self) -> dict[str, Any]:
        return {"user_id": str(self.user_id), "jti": str(self.jti)}


class RefreshTokenSchema(BaseModel):
    user_id: UUID
    jti: UUID
