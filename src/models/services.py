from sqlalchemy import (
    Column,
    String,
)

from src.db import Base


class VolunteerServiceModel(Base):
    name = Column(String(100), nullable=False)
