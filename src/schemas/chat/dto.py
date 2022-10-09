from datetime import date
from typing import Literal
from uuid import UUID

from src.enums.chat import RequestStatus
from src.schemas.base import BaseModel


class ChatUser(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    date_of_birth: date


class Chat(BaseModel):
    id: UUID
    user: ChatUser
    requester_id: UUID
    status: RequestStatus
    has_unread_messages: bool


class MessageRequest(BaseModel):
    message: str


class Message(BaseModel):
    sender_id: UUID
    message: str


class ChatDetailResponse(BaseModel):
    id: UUID
    has_unread_messages: bool
    user_data: ChatUser


class ChatCreateRequestSchema(BaseModel):
    user_id: UUID


class ChatUpdateStatusRequestSchema(BaseModel):
    status: Literal["ACCEPTED", "REJECTED"]


class ChatMessageResponse(BaseModel):
    id: UUID
    sender_id: UUID
    message: str


class ChatFilterParams(BaseModel):
    status: Literal["PENDING"] = None
