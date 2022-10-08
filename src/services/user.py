import random
from datetime import (
    datetime,
    timedelta,
)
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
from src.schemas.user.data_access import (
    UserInputSchema,
    UserSchema,
    UserUpdateSchema,
)
from src.schemas.user.dto import (
    UserRegisterSchema,
    UserResponseSchema,
)
from src.settings import settings
from src.utils.images import (
    remove_file_from_s3,
    remove_file_locally,
    save_image_locally,
    upload_image_to_s3,
)
from src.utils.password import password_context
from src.utils.sns import send_otp


class UserService:
    def __init__(self, user_data_access: UserDataAccess = Depends()):
        self._user_data_access = user_data_access

    async def register_user(self, input_schema: UserRegisterSchema) -> UserResponseSchema:
        input_schema.password = password_context.hash(input_schema.password)
        return UserResponseSchema.from_orm(
            await self._user_data_access.register_user(
                input_schema=UserInputSchema.parse_obj({**input_schema.dict(), "is_verified": False})
            )
        )

    async def get_user(self, user_id: UUID) -> UserResponseSchema:
        return UserResponseSchema.from_orm(await self._user_data_access.get_by_id(id=user_id))

    async def update_user(
        self, user: UserSchema, update_schema: UserUpdateSchema, user_id: UUID
    ) -> UserResponseSchema:
        update_schema = data_access_schemas.UserUpdateSchema(**update_schema.dict(), is_verified=user.is_verified)
        return UserResponseSchema.from_orm(
            await self._user_data_access.update(update_schema=update_schema, id=user_id)
        )

    async def generate_otp(self, user: UserSchema) -> None:
        if user.phone_number is None:
            raise HTTPException(status_code=400, detail="You need to provide a phone number before")

        if user.is_verified:
            raise HTTPException(status_code=400, detail="Your account is verified")

        otp_code = random.randint(100000, 999999)
        otp_code_issued_at = datetime.utcnow()

        await self._user_data_access.update(
            update_schema=UserUpdateSchema(
                **{
                    **user.dict(),
                    "otp_code": otp_code,
                    "otp_code_issued_at": otp_code_issued_at,
                }
            ),
            id=user.id,
        )

        if settings.debug:
            print(f"OTP: {otp_code}")
        else:
            await send_otp(phone_number=user.phone_number, otp=otp_code)

    async def confirm_otp(self, user: UserSchema, otp: int) -> None:
        if user.is_verified:
            raise HTTPException(status_code=400, detail="Your account is verified")

        if user.otp_code != otp or user.otp_code_issued_at + timedelta(minutes=5) < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Invalid OTP code")

        await self._user_data_access.update(
            update_schema=UserUpdateSchema(
                **{
                    **user.dict(),
                    "is_verified": True,
                }
            ),
            id=user.id,
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
