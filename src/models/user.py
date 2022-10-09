from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from src.db import Base
from src.enums.roles import UserRole


class UserModel(Base):
    email = Column(String(length=100), nullable=False, unique=True)
    password = Column(String(length=100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(50), nullable=True)
    image = Column(String(), nullable=True)
    is_verified = Column(Boolean(), nullable=False, default=False)
    otp_code = Column(Integer, nullable=True)
    otp_code_issued_at = Column(DateTime, nullable=True)
    role = Column(String(20), nullable=False, default=UserRole.STANDARD.value)

    send_requests = relationship(
        "ChatRequestModel", back_populates="requester", foreign_keys="ChatRequestModel.requester_id"
    )
    requests = relationship(
        "ChatRequestModel", back_populates="requested", foreign_keys="ChatRequestModel.requested_id"
    )
