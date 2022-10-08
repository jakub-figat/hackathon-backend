from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    UploadFile,
    status,
)

from src.deps.jwt import get_request_user
from src.exceptions.data_access import ObjectAlreadyExists
from src.schemas.user.data_access import UserSchema
from src.schemas.user.dto import (
    OTPConfirmRequest,
    UserRegisterSchema,
    UserResponseSchema,
    UserUpdateSchema,
)
from src.services.user import UserService


user_router = APIRouter(tags=["users"])


@user_router.post("/register/", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
async def create_user(schema: UserRegisterSchema, user_service: UserService = Depends()) -> UserResponseSchema:
    try:
        return await user_service.register_user(input_schema=schema)
    except ObjectAlreadyExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The email is already in use.")


@user_router.get(
    "/me/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchema,
)
async def get_user(user: UserSchema = Depends(get_request_user)) -> UserResponseSchema:
    return UserResponseSchema.parse_obj(user)


@user_router.put("/me/", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def update_user(
    update_schema: UserUpdateSchema,
    user: UserSchema = Depends(get_request_user),
    user_service: UserService = Depends(),
) -> UserResponseSchema:
    return await user_service.update_user(user=user, update_schema=update_schema, user_id=user.id)


@user_router.post("/me/generate-otp/", status_code=status.HTTP_204_NO_CONTENT)
async def generate_otp(user: UserSchema = Depends(get_request_user), user_service: UserService = Depends()):
    return await user_service.generate_otp(user=user)


@user_router.post("/me/confirm-otp/", status_code=status.HTTP_204_NO_CONTENT)
async def generate_otp(
    schema: OTPConfirmRequest, user: UserSchema = Depends(get_request_user), user_service: UserService = Depends()
):
    return await user_service.confirm_otp(user=user, otp=schema.otp)


@user_router.put("/me/image/", status_code=status.HTTP_200_OK)
async def update_user_image(
    image_file: UploadFile, user_service: UserService = Depends(), user: UserSchema = Depends(get_request_user)
) -> Response:
    await user_service.save_user_image(image_file=image_file, user_id=user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
