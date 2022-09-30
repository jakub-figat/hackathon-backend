from uuid import UUID

from fastapi import Depends

from src.data_access.user import UserDataAccess
from src.schemas.user import (
    UserRegisterSchema,
    UserSchema,
)


class UserService:
    def __init__(self, user_data_access: UserDataAccess = Depends()):
        self._user_data_access = user_data_access

    async def register_user(self, input_schema: UserRegisterSchema) -> UserSchema:
        return await self._user_data_access.register_user(input_schema=input_schema)

    async def get_user(self, user_id: UUID) -> UserSchema:
        return await self._user_data_access.get_by_id(id=user_id)
