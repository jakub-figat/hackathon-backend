from sqlalchemy import (
    Column,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db import Base


class RefreshTokenModel(Base):
    user_id = Column(UUID, ForeignKey("usermodels.id"))
    jti = Column(UUID, nullable=False)

    user = relationship("UserModel")
