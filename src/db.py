import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declared_attr, as_declarative

from src.settings import settings


engine = create_async_engine(url=settings.database_url, echo=True)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=AsyncSession)


@as_declarative()
class Base:
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"
