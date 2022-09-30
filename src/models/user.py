from sqlalchemy import Column, Date, String

from src.db import Base


class UserModel(Base):
    email = Column(String(length=100), nullable=False, unique=True)
    password = Column(String(length=100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
