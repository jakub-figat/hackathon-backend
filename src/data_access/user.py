from uuid import UUID

from src.data_access.base import BaseAsyncPostgresDataAccess
from src.models.user import UserModel
from src.schemas.user.data_access import (
    UserInputSchema,
    UserSchema,
    UserUpdateSchema,
)


class UserDataAccess(BaseAsyncPostgresDataAccess[UserModel, UserInputSchema, UserSchema]):
    _input_schema = UserInputSchema
    _output_schema = UserSchema
    _model = UserModel

    async def register_user(self, input_schema: UserInputSchema) -> UserSchema:
        return await self.create(input_schema=input_schema)

    async def update_user(self, update_schema: UserUpdateSchema, user_id: UUID) -> UserSchema:
        user = await self.get_by_id(id=user_id)
        for key, value in update_schema.to_orm_kwargs().items():
            setattr(user, key, value)

        await self._session.commit()

        return user
