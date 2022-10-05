from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from src.deps.jwt import get_request_user
from src.exceptions.data_access import ObjectAlreadyExists
from src.schemas.user.data_access import UserSchema
from src.schemas.user.dto import (
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
    return await user_service.update_user(update_schema=update_schema, user_id=user.id)
