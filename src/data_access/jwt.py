from uuid import UUID

from sqlalchemy import (
    delete,
    select,
)

from src import RefreshTokenModel
from src.data_access.base import BaseAsyncPostgresDataAccess
from src.exceptions.data_access import ObjectNotFound
from src.schemas.jwt.data_access import (
    RefreshTokenInputSchema,
    RefreshTokenSchema,
)


class RefreshTokenDataAccess(
    BaseAsyncPostgresDataAccess[RefreshTokenModel, RefreshTokenInputSchema, RefreshTokenSchema]
):
    _input_schema = RefreshTokenInputSchema
    _output_schema = RefreshTokenSchema
    _model = RefreshTokenModel

    async def delete_by_jti(self, jti: UUID) -> None:
        statement = delete(self._model).where(self._model.jti == jti)
        if (await self._session.scalar(select(self._model).where(self._model.jti == jti))) is None:
            raise ObjectNotFound(f"The object with id={jti} does not exist.")

        await self._session.execute(statement)
