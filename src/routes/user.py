from fastapi import (
    APIRouter,
    status,
)

from src.schemas.user import (
    UserRegisterSchema,
    UserSchema,
)


user_router = APIRouter(tags=["users"])


@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user(schema: UserRegisterSchema) -> UserSchema:
    pass


@user_router.get("/", status_code=status.HTTP_200_OK)
async def get_users() -> list[UserSchema]:
    return []
