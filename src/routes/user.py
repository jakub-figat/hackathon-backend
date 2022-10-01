from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from src.deps.jwt import get_request_user
from src.exceptions.data_access import (
    ModelAlreadyExists,
    ModelNotFound,
)
from src.schemas.user import (
    AccessTokenSchema,
    UserLoginSchema,
    UserRegisterSchema,
    UserResponseSchema,
    UserSchema,
)
from src.services.user import UserService


user_router = APIRouter(tags=["users"])


@user_router.post("/register/", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
async def create_user(schema: UserRegisterSchema, user_service: UserService = Depends()) -> UserResponseSchema:
    try:
        return await user_service.register_user(input_schema=schema)
    except ModelAlreadyExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The email is already in use.")


@user_router.get("/{user_id}/", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def get_user(
    user_id: UUID, user_service: UserService = Depends(), user: UserSchema = Depends(get_request_user)
) -> UserResponseSchema:
    print(user.email)
    try:
        return await user_service.get_user(user_id=user_id)
    except ModelNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist.")


@user_router.post("/login/", status_code=status.HTTP_200_OK, response_model=AccessTokenSchema)
async def login(schema: UserLoginSchema, user_service: UserService = Depends()) -> AccessTokenSchema:
    try:
        return await user_service.generate_access_token(login_schema=schema)
    except ModelNotFound:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials.")
