from typing import Any

from fastapi import (
    Depends,
    HTTPException,
)
from starlette import status

from src.data_access.user import UserDataAccess
from src.exceptions.data_access import ModelNotFound
from src.schemas.user import UserSchema
from src.utils.jwt import (
    InvalidAccessToken,
    decode_jwt,
    oauth2_scheme,
)


def require_auth(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    try:
        return decode_jwt(token=token)
    except InvalidAccessToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The provided token is invalid.")


async def get_request_user(
    token_data: dict[str, Any] = Depends(require_auth), user_data_access: UserDataAccess = Depends()
) -> UserSchema:
    user_id = token_data["sub"]

    try:
        return UserSchema.from_orm(await user_data_access.get_by_id(id=user_id))
    except ModelNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist.")
