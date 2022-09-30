import datetime as dt

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data_access.user import UserDataAccess
from src.schemas.user import UserRegisterSchema


@pytest_asyncio.fixture(scope="function")
async def user_data_access(async_test_session: AsyncSession) -> UserDataAccess:
    return UserDataAccess(session=async_test_session)


@pytest.mark.asyncio
async def test_user_data_access_create_and_get_user_by_id(user_data_access: UserDataAccess) -> None:
    register_schema = UserRegisterSchema(
        email="test@test.com",
        date_of_birth=dt.date(2000, 1, 1),
        password="password12345",
        password_2="password12345",
    )

    user = await user_data_access.register_user(input_schema=register_schema)
    user_from_db = await user_data_access.get_by_id(id=user.id)
    assert user == user_from_db
