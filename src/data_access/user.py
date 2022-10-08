from uuid import UUID

from sqlalchemy import update

from src.data_access.base import BaseAsyncPostgresDataAccess
from src.models.user import UserModel
from src.schemas.user.data_access import (
    UserInputSchema,
    UserSchema,
)


class UserDataAccess(BaseAsyncPostgresDataAccess[UserModel, UserInputSchema, UserSchema]):
    _input_schema = UserInputSchema
    _output_schema = UserSchema
    _model = UserModel

    async def register_user(self, input_schema: UserInputSchema) -> UserSchema:
        return await self.create(input_schema=input_schema)

    async def update_user_image(self, image_path: str, user_id: UUID) -> None:
        await self._session.execute(update(self._model).where(self._model.id == user_id).values(image=image_path))
        await self._session.commit()
