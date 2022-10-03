from fastapi import Depends
from jose import JWTError

from src.data_access.jwt import RefreshTokenDataAccess
from src.data_access.user import UserDataAccess
from src.enums.jwt import TokenType
from src.exceptions.data_access import ObjectNotFound
from src.exceptions.jwt import InvalidToken
from src.exceptions.user import InvalidCredentials
from src.schemas.jwt.data_access import RefreshTokenInputSchema
from src.schemas.jwt.dto import TokenPairSchema
from src.schemas.user.dto import UserLoginSchema
from src.utils.jwt import (
    decode_jwt,
    generate_token_pair,
)
from src.utils.password import password_context


class TokenService:
    def __init__(
        self,
        user_data_access: UserDataAccess = Depends(),
        refresh_token_data_access: RefreshTokenDataAccess = Depends(),
    ) -> None:
        self._user_data_access = user_data_access
        self._refresh_token_data_access = refresh_token_data_access

    async def generate_token_pair(self, login_schema: UserLoginSchema) -> TokenPairSchema:
        user = await self._user_data_access.get_by(email=login_schema.email)

        if not password_context.verify(secret=login_schema.password, hash=user.password):
            raise InvalidCredentials("Provided credentials are invalid")

        token_pair = generate_token_pair(user_id=user.id)

        await self._refresh_token_data_access.create(
            RefreshTokenInputSchema(
                user_id=user.id, jti=decode_jwt(token_pair.refresh_token, token_type=TokenType.refresh)["jti"]
            ),
        )

        return token_pair

    async def refresh_token_pair(self, refresh_token: str) -> TokenPairSchema:
        try:
            refresh_token_data = decode_jwt(token=refresh_token, token_type=TokenType.refresh)
        except JWTError:
            raise InvalidToken("Invalid refresh token")

        token_pair = generate_token_pair(user_id=refresh_token_data["sub"])

        try:
            await self._refresh_token_data_access.delete_by_jti(jti=refresh_token_data["jti"])
        except ObjectNotFound:
            raise InvalidToken("Invalid refresh token")

        await self._refresh_token_data_access.create(
            RefreshTokenInputSchema(
                user_id=refresh_token_data["sub"],
                jti=decode_jwt(token_pair.refresh_token, token_type=TokenType.refresh)["jti"],
            )
        )

        return token_pair
