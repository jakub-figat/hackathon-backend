from uuid import (
    UUID,
    uuid4,
)

from fastapi import (
    Depends,
    UploadFile,
)

from src.data_access.user import UserDataAccess
from src.schemas.user import data_access as data_access_schemas
from src.schemas.user.data_access import UserInputSchema
from src.schemas.user.dto import (
    UserRegisterSchema,
    UserResponseSchema,
    UserUpdateSchema,
)
from src.settings import settings
from src.utils.images import (
    remove_file_from_s3,
    remove_file_locally,
    save_image_locally,
    upload_image_to_s3,
)
from src.utils.password import password_context


class UserService:
    def __init__(self, user_data_access: UserDataAccess = Depends()):
        self._user_data_access = user_data_access

    async def register_user(self, input_schema: UserRegisterSchema) -> UserResponseSchema:
        input_schema.password = password_context.hash(input_schema.password)
        return UserResponseSchema.from_orm(
            await self._user_data_access.register_user(input_schema=UserInputSchema.parse_obj(input_schema))
        )

    async def get_user(self, user_id: UUID) -> UserResponseSchema:
        return UserResponseSchema.from_orm(await self._user_data_access.get_by_id(id=user_id))

    async def update_user(self, update_schema: UserUpdateSchema, user_id: UUID) -> UserResponseSchema:
        update_schema = data_access_schemas.UserUpdateSchema(**update_schema.dict())
        return UserResponseSchema.from_orm(
            await self._user_data_access.update(update_schema=update_schema, id=user_id)
        )

    async def save_user_image(self, image_file: UploadFile, user_id: UUID) -> None:
        user = await self._user_data_access.get_by_id(id=user_id)
        if user.image is not None:
            await (remove_file_locally(user.image) if settings.debug else remove_file_from_s3(user.image))

        image_path = await (
            save_image_locally(image_uuid=uuid4(), image_file=image_file)
            if settings.debug
            else upload_image_to_s3(image_uuid=uuid4(), image_file=image_file)
        )
        await self._user_data_access.update_user_image(image_path=image_path, user_id=user_id)
