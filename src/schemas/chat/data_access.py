from typing import Any
from uuid import UUID

from src.enums.chat import RequestStatus
from src.schemas.base import BaseModel
from src.utils.schemas import BaseInputSchema


class ChatRequestInputSchema(BaseInputSchema):
    requester_id: UUID
    requested_id: UUID
    status: RequestStatus
    has_unread_messages: bool

    def to_orm_kwargs(self) -> dict[str, Any]:
        return {
            "requester_id": str(self.requester_id),
            "requested_id": str(self.requester_id),
            "status": self.status.value,
            **self.dict(exclude={"requester_id", "requested_id", "status"}),
        }


class ChatRequestSchema(BaseModel):
    chat_id: UUID
    sender_id: UUID
    message: str
