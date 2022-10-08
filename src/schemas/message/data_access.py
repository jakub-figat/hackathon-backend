from typing import Any
from uuid import UUID

from src.schemas.base import BaseModel
from src.utils.schemas import BaseInputSchema


class ChatMessageInputSchema(BaseInputSchema):
    chat_id: UUID
    sender_id: UUID
    message: str

    def to_orm_kwargs(self) -> dict[str, Any]:
        return {
            "chat_id": str(self.chat_id),
            "sender_id": str(self.chat_id),
            **self.dict(exclude={"chat_id", "sender_id"}),
        }


class ChatMessageSchema(BaseModel):
    id: UUID
    chat_id: UUID
    sender_id: UUID
    message: str
