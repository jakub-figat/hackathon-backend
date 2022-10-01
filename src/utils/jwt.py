import datetime as dt
import uuid
from typing import Any

from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import (
    JWTError,
    jwt,
)

from src.enums.jwt import TokenType
from src.schemas.user import (
    TokenPairSchema,
    UserSchema,
)
from src.settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/login/")


class InvalidAccessToken(Exception):
    """Error raised when an invalid token was provided."""


def generate_token_pair(user_id: uuid.UUID) -> TokenPairSchema:
    datetime = dt.datetime.utcnow()
    token_data = {
        "iat": datetime,
        "sub": str(user_id),
    }
    return TokenPairSchema(
        access_token=jwt.encode(
            claims={
                "jti": str(uuid.uuid4()),
                "type": TokenType.access.value,
                "exp": datetime + dt.timedelta(settings.token_expiration_time),
                **token_data,
            },
            key=settings.token_secret_key,
        ),
        refresh_token=jwt.encode(
            claims={
                "jti": str(uuid.uuid4()),
                "type": TokenType.refresh.value,
                "exp": datetime + dt.timedelta(settings.refresh_expiration_time),
                **token_data,
            },
            key=settings.token_secret_key,
        ),
    )


def decode_jwt(token: str, token_type: str = TokenType.access) -> dict[str, Any]:
    try:
        token_data = jwt.decode(token=token, key=settings.token_secret_key)
        if TokenType(token_data["type"]) != token_type:
            raise JWTError("Invalid token type")
        return token_data
    except JWTError:
        raise InvalidAccessToken("The provided token is invalid.")
