from fastapi import Depends
from jose import JWTError

from src.data_access.user import UserDataAccess
from src.enums.jwt import TokenType
from src.exceptions.jwt import InvalidToken
from src.exceptions.user import InvalidCredentials
from src.schemas.user import (
    TokenPairSchema,
    UserLoginSchema,
)
from src.utils.jwt import (
    decode_jwt,
    generate_token_pair,
)
from src.utils.password import password_context


class TokenService:
    def __init__(self, user_data_access: UserDataAccess = Depends()) -> None:
        self._user_data_access = user_data_access

    async def generate_token_pair(self, login_schema: UserLoginSchema) -> TokenPairSchema:
        user = await self._user_data_access.get_by(email=login_schema.email)

        if not password_context.verify(secret=login_schema.password, hash=user.password):
            raise InvalidCredentials("Provided credentials are invalid")

        return generate_token_pair(user_id=user.id)

    @classmethod
    def refresh_token_pair(cls, refresh_token: str) -> TokenPairSchema:
        try:
            refresh_token_data = decode_jwt(token=refresh_token, token_type=TokenType.refresh)
        except JWTError:
            raise InvalidToken("Invalid refresh token")

        return generate_token_pair(refresh_token_data["sub"])
