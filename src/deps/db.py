from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Session


async def get_async_session() -> Iterable[AsyncSession]:
    async with Session() as session:
        yield session
