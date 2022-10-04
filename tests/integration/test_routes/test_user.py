import datetime as dt
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import app
from src.data_access.user import UserDataAccess
from src.deps.db import get_async_session
from src.deps.jwt import get_request_user
from src.schemas.user.data_access import (
    UserInputSchema,
    UserSchema,
)
from src.schemas.user.dto import UserUpdateSchema


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


@pytest.fixture
def user_schema() -> UserSchema:
    return UserSchema(
        id=uuid4(),
        email="test@test.com",
        date_of_birth=dt.date(2000, 1, 1),
        password="password12345678",
        first_name="Jacek",
        last_name="Gardziel",
    )


@pytest.fixture
def update_user_schema() -> UserUpdateSchema:
    return UserUpdateSchema(
        date_of_birth=dt.date(2020, 5, 5),
        first_name="Jacek",
        last_name="Smierdziel",
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
    await data_access.register_user(input_schema=register_schema)
    return data_access


@pytest.fixture(scope="function")
async def override_get_request_user_dependency(user_schema: UserSchema) -> None:
    app.dependency_overrides[get_request_user] = lambda: user_schema
    yield
    app.dependency_overrides[get_request_user] = get_request_user


@pytest.fixture(scope="function")
async def override_get_request_user_dependency_with_data_access(user_data_access_with_user: UserDataAccess) -> None:
    user_schema = (await user_data_access_with_user.get_many())[0]
    app.dependency_overrides[get_request_user] = lambda: user_schema
    yield
    app.dependency_overrides[get_request_user] = get_request_user


async def test_user_routes_register_user(register_schema: UserInputSchema, http_client: AsyncClient) -> None:
    response = await http_client.post(url="/users/register/", json=jsonable_encoder(register_schema.dict()))
    assert response.status_code == status.HTTP_201_CREATED
    response_body = response.json()

    assert "id" in response_body
    assert response_body["firstName"] == register_schema.first_name
    assert response_body["lastName"] == register_schema.last_name


async def test_user_routes_register_user_returns_unprocessable_entity_on_invalid_request_body(
    register_schema: UserInputSchema, http_client: AsyncClient
) -> None:
    register_schema.password = "xD"
    response = await http_client.post("/users/register/", json=jsonable_encoder(register_schema.dict()))

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_user_routes_me(
    override_get_request_user_dependency, user_schema: UserSchema, http_client: AsyncClient
) -> None:
    response = await http_client.get("/users/me/")
    assert response.status_code == status.HTTP_200_OK

    assert response.json()["id"] == str(user_schema.id)


async def test_user_routes_update_user(
    http_client: AsyncClient,
    update_user_schema: UserUpdateSchema,
    user_data_access_with_user: UserDataAccess,
    override_get_request_user_dependency_with_data_access,
) -> None:
    response = await http_client.put(url="/users/me/", json=jsonable_encoder(update_user_schema.dict()))
    assert response.status_code == status.HTTP_200_OK

    assert response.json()["lastName"] == "Smierdziel"
