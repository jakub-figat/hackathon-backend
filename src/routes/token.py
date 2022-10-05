from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Response,
    status,
)

from src.exceptions.data_access import ObjectNotFound
from src.exceptions.jwt import InvalidToken
from src.schemas.user.dto import UserLoginSchema
from src.services.jwt import TokenService
from src.settings import settings


token_router = APIRouter(tags=["tokens"])


@token_router.post("/login/", status_code=status.HTTP_200_OK)
async def login(
    schema: UserLoginSchema, response: Response, token_service: TokenService = Depends()
) -> dict[str, str]:
    try:
        token_pair = await token_service.generate_token_pair(login_schema=schema)

        response.set_cookie(
            key="refresh_token",
            value=token_pair.refresh_token,
            expires=settings.refresh_expiration_time,
            httponly=True,
        )
        response.set_cookie(
            key="access_token",
            value=token_pair.access_token,
            expires=settings.token_expiration_time,
            httponly=True,
        )

        return {"detail": "Successfully logged in"}
    except ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials.")


@token_router.post("/refresh/", status_code=status.HTTP_200_OK)
async def refresh_token_pair(
    response: Response, refresh_token: str = Cookie(), token_service: TokenService = Depends()
) -> dict[str, str]:
    try:
        token_pair = await token_service.refresh_token_pair(refresh_token=refresh_token)

        response.set_cookie(
            key="refresh_token",
            value=token_pair.refresh_token,
            expires=settings.refresh_expiration_time,
            httponly=True,
        )
        response.set_cookie(
            key="access_token",
            value=token_pair.access_token,
            expires=settings.token_expiration_time,
            httponly=True,
        )

        return {"detail": "Successfully logged in"}
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
