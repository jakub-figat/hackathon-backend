from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Response,
    status,
)

from src.exceptions.data_access import ObjectNotFound
from src.schemas.jwt.dto import AccessTokenSchema
from src.schemas.user.dto import UserLoginSchema
from src.services.jwt import TokenService


token_router = APIRouter(tags=["tokens"])


@token_router.post("/login/", status_code=status.HTTP_200_OK, response_model=AccessTokenSchema)
async def login(
    schema: UserLoginSchema, response: Response, token_service: TokenService = Depends()
) -> AccessTokenSchema:
    try:
        token_pair = await token_service.generate_token_pair(login_schema=schema)
        response.set_cookie(key="refresh_token", value=token_pair.refresh_token, secure=True, httponly=True)

        return AccessTokenSchema(access_token=token_pair.access_token)
    except ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials.")


@token_router.post("/refresh/", status_code=status.HTTP_200_OK, response_model=AccessTokenSchema)
async def refresh_token_pair(
    response: Response, refresh_token: str = Cookie(...), token_service: TokenService = Depends()
) -> AccessTokenSchema:
    token_pair = token_service.refresh_token_pair(refresh_token=refresh_token)
    response.set_cookie(key="refresh_token", value=token_pair.refresh_token)

    return AccessTokenSchema(access_token=token_pair.access_token)
