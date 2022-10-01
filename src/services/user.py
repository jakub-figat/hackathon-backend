from uuid import UUID

from fastapi import Depends

from src.data_access.user import UserDataAccess
from src.schemas.user import (
    AccessTokenSchema,
    UserLoginSchema,
    UserRegisterSchema,
    UserResponseSchema,
)
from src.utils.jwt import generate_jwt
from src.utils.password import password_context


class UserService:
    def __init__(self, user_data_access: UserDataAccess = Depends()):
        self._user_data_access = user_data_access

    async def register_user(self, input_schema: UserRegisterSchema) -> UserResponseSchema:
        input_schema.password = password_context.hash(input_schema.password)
        return UserResponseSchema.from_orm(await self._user_data_access.register_user(input_schema=input_schema))

    async def get_user(self, user_id: UUID) -> UserResponseSchema:
        return UserResponseSchema.from_orm(await self._user_data_access.get_by_id(id=user_id))

    async def generate_access_token(self, login_schema: UserLoginSchema) -> AccessTokenSchema:
        user = await self._user_data_access.get_by(email=login_schema.email)

        if not password_context.verify(secret=login_schema.password, hash=user.password):
            raise Exception

        return AccessTokenSchema(access_token=generate_jwt(user_schema=user))
