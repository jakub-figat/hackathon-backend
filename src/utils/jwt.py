import datetime as dt
import uuid
from typing import Any

from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import (
    JWTError,
    jwt,
)

from src.schemas.user import UserSchema
from src.settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


class InvalidAccessToken(Exception):
    """Error raised when an invalid token was provided."""


def generate_jwt(user_schema: UserSchema) -> str:
    datetime = dt.datetime.utcnow()
    user_data = {
        "iat": datetime,
        "exp": datetime + dt.timedelta(minutes=settings.token_expiration_time),
        "sub": str(user_schema.id),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(claims=user_data, key=settings.token_secret_key)


def decode_jwt(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token=token, key=settings.token_secret_key)
    except JWTError:
        raise InvalidAccessToken("The provided token is invalid.")
