from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db import Base
from src.enums.chat import RequestStatus


class ChatRequestModel(Base):
    requester_id = Column(UUID(as_uuid=True), ForeignKey("usermodels.id"), nullable=False)
    requested_id = Column(UUID(as_uuid=True), ForeignKey("usermodels.id"), nullable=False)
    status = Column(String(20), nullable=False, default=RequestStatus.PENDING.value)
    has_unread_messages = Column(Boolean, nullable=False, default=False)

    requester = relationship("UserModel", foreign_keys=[requester_id])
    requested = relationship("UserModel", foreign_keys=[requested_id])
    messages = relationship("ChatMessageModel", back_populates="chat")


class ChatMessageModel(Base):
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chatrequestmodels.id"))
    sender_id = Column(UUID(as_uuid=True), ForeignKey("usermodels.id"))
    message = Column(String(512), nullable=False)

    chat = relationship("ChatRequestModel", back_populates="messages", foreign_keys=[chat_id])
    sender = relationship("UserModel", foreign_keys=[sender_id])
