from typing import Any

from fastapi import (
    Cookie,
    Depends,
    HTTPException,
)
from starlette import status

from src.data_access.user import UserDataAccess
from src.exceptions.data_access import ObjectNotFound
from src.exceptions.jwt import InvalidToken
from src.schemas.user.data_access import UserSchema
from src.utils.jwt import decode_jwt


def require_auth(access_token: str = Cookie(...)) -> dict[str, Any]:
    try:
        return decode_jwt(token=access_token)
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The provided token is invalid.")


async def get_request_user(
    token_data: dict[str, Any] = Depends(require_auth), user_data_access: UserDataAccess = Depends()
) -> UserSchema:
    user_id = token_data["sub"]
    try:
        return UserSchema.from_orm(await user_data_access.get_by_id(id=user_id))
    except ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist.")
