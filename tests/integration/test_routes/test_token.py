import datetime as dt

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import app
from src.data_access.user import UserDataAccess
from src.deps.db import get_async_session
from src.schemas.user.data_access import UserInputSchema
from src.utils.password import password_context


pytestmark = pytest.mark.integration


@pytest.fixture
def register_schema() -> UserInputSchema:
    return UserInputSchema(
        email="test@test.com",
        date_of_birth=dt.date(2000, 1, 1),
        password="password12345678",
        first_name="Jacek",
        last_name="Gardziel",
    )


@pytest.fixture(scope="function", autouse=True)
async def override_get_async_session(async_test_session: AsyncSession) -> None:
    app.dependency_overrides[get_async_session] = lambda: async_test_session
    yield
    app.dependency_overrides[get_async_session] = lambda: get_async_session


@pytest.fixture(scope="function")
async def user_data_access_with_user(
    register_schema: UserInputSchema, async_test_session: AsyncSession
) -> UserDataAccess:
    data_access = UserDataAccess(session=async_test_session)
    register_schema_copy = register_schema.copy()
    register_schema_copy.password = password_context.hash(register_schema.password)
    await data_access.register_user(input_schema=register_schema_copy)
    return data_access


async def test_token_routes_login(
    http_client: AsyncClient, register_schema: UserInputSchema, user_data_access_with_user: UserDataAccess
) -> None:
    response = await http_client.post(url="/token/login/", json=register_schema.dict(include={"email", "password"}))
    assert response.status_code == status.HTTP_200_OK

    assert "refresh_token" in response.cookies
    assert "access_token" in response.cookies
