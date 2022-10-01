from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from src.deps.jwt import require_auth
from src.exceptions.data_access import (
    ObjectAlreadyExists,
    ObjectNotFound,
)
from src.schemas.user.dto import (
    UserRegisterSchema,
    UserResponseSchema,
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
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchema,
    dependencies=[Depends(require_auth)],
)
async def get_user(user_id: UUID, user_service: UserService = Depends()) -> UserResponseSchema:
    try:
        return await user_service.get_user(user_id=user_id)
    except ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist.")
