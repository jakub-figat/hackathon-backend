from uuid import UUID

from sqlalchemy import select

from src import VolunteerProfileModel
from src.data_access.base import BaseAsyncPostgresDataAccess
from src.exceptions.data_access import ObjectNotFound
from src.schemas.volunteer_profile.data_access import (
    VolunteerProfileInputSchema,
    VolunteerProfileSchema,
)


class VolunteerProfileDataAccess(
    BaseAsyncPostgresDataAccess[VolunteerProfileModel, VolunteerProfileInputSchema, VolunteerProfileSchema]
):
    _model = VolunteerProfileModel
    _input_schema = VolunteerProfileInputSchema
    _output_schema = VolunteerProfileSchema

    async def get_by_user_id(self, user_id: UUID) -> VolunteerProfileSchema:
        statement = select(self._model).where(self._model.user_id == user_id)

        if (model := (await self._session.scalar(statement))) is None:
            raise ObjectNotFound(f"The object with user_id={id} does not exist.")

        return self._output_schema.from_orm(model)
