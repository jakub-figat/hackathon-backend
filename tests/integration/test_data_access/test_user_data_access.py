import datetime as dt
import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.data_access.base import (
    ObjectAlreadyExists,
    ObjectNotFound,
)
from src.data_access.user import UserDataAccess
from src.schemas.user.data_access import UserInputSchema


pytestmark = pytest.mark.integration


@pytest.fixture
def register_schema() -> UserInputSchema:
    return UserInputSchema(
        email="test@test.com",
        date_of_birth=dt.date(2000, 1, 1),
        password="password12345",
    )


@pytest.fixture(scope="function")
async def user_data_access(async_test_session: AsyncSession) -> UserDataAccess:
    return UserDataAccess(session=async_test_session)


async def test_user_data_access_create_and_get_user_by_id(
    register_schema: UserInputSchema, user_data_access: UserDataAccess
) -> None:
    user = await user_data_access.register_user(input_schema=register_schema)
    user_from_db = await user_data_access.get_by_id(id=user.id)
    assert user == user_from_db


async def test_user_data_access_get_returns_empty_list(user_data_access: UserDataAccess) -> None:
    users = await user_data_access.get_many()
    assert users == []


@pytest.mark.parametrize(
    "data,match",
    (
        ({"id": "0ee1a2be-5031-4b42-b399-1a455c7a1390"}, r"id=0ee1a2be-5031-4b42-b399-1a455c7a1390"),
        ({"email": "user@example.com"}, r"email=user@example.com"),
        (
            {"id": "0ee1a2be-5031-4b42-b399-1a455c7a1390", "email": "user@example.com"},
            r"id=0ee1a2be-5031-4b42-b399-1a455c7a1390, email=user@example.com",
        ),
    ),
)
async def test_user_data_access_get_by_raises_object_not_found_exception(
    data, match, user_data_access: UserDataAccess
) -> None:
    with pytest.raises(ObjectNotFound, match=match):
        await user_data_access.get_by(**data)


async def test_user_data_access_get_with_one_user(
    register_schema: UserInputSchema, user_data_access: UserDataAccess
) -> None:
    await user_data_access.register_user(input_schema=register_schema)
    users = await user_data_access.get_many()
    assert len(users) == 1


async def test_user_data_access_create_and_delete_user(
    register_schema: UserInputSchema, user_data_access: UserDataAccess
) -> None:
    user = await user_data_access.register_user(input_schema=register_schema)
    await user_data_access.delete_by_id(id=user.id)
    assert await user_data_access.get_many() == []


async def test_user_data_access_raises_model_not_found_when_user_does_not_exist(
    user_data_access: UserDataAccess,
) -> None:
    with pytest.raises(ObjectNotFound):
        await user_data_access.get_by_id(id=uuid.uuid4())


async def test_user_data_access_raises_model_not_found_when_deleting_not_existing_user(
    user_data_access: UserDataAccess,
) -> None:
    with pytest.raises(ObjectNotFound):
        await user_data_access.delete_by_id(id=uuid.uuid4())


async def test_user_data_access_raises_model_already_exists_when_email_is_already_occupied(
    register_schema: UserInputSchema, user_data_access: UserDataAccess
) -> None:
    await user_data_access.register_user(input_schema=register_schema)
    with pytest.raises(ObjectAlreadyExists):
        await user_data_access.register_user(input_schema=register_schema)
