import asyncio
from typing import AsyncIterable, Iterable

import pytest
import pytest_asyncio
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from src.db import Base
from src.settings import settings


@pytest.fixture(scope="session")
def event_loop() -> Iterable[asyncio.AbstractEventLoop]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_database() -> None:
    with create_engine(
        url=(
            f"postgresql://{settings.postgres_user}:{settings.postgres_password}"
            f"@{settings.postgres_host}/{settings.postgres_database}"
        )
    ).connect() as connection:
        connection.execute("commit")
        connection.execute(f"create database {settings.postgres_database}_test")

        yield
        connection.execute("commit")
        connection.execute(f"drop database {settings.postgres_database}_test")


@pytest_asyncio.fixture(scope="session")
async def async_test_engine(test_database) -> AsyncIterable[AsyncEngine]:
    async_engine = create_async_engine(
        url=(
            f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
            f"@{settings.postgres_host}/{settings.postgres_database}"
        ),
    )

    yield async_engine
    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_test_session(async_test_engine: AsyncEngine, test_database) -> AsyncIterable[AsyncSession]:
    async with async_test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with AsyncSession(bind=async_test_engine, expire_on_commit=False) as async_session:
        await async_session.begin()
        yield async_session
        await async_session.rollback()

    async with async_test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
