import datetime as dt
from uuid import UUID

from sqlalchemy import (
    and_,
    func,
    select,
)
from sqlalchemy.dialects import postgresql as pg

from src import VolunteerProfileModel
from src.data_access.base import BaseAsyncPostgresDataAccess
from src.exceptions.data_access import ObjectNotFound
from src.models.volunteer_profile import volunteer_profile_to_service
from src.schemas.volunteer_profile.data_access import (
    VolunteerProfileInputSchema,
    VolunteerProfileSchema,
)
from src.schemas.volunteer_profile.dto import VolunteerProfileFilterParams


class VolunteerProfileDataAccess(
    BaseAsyncPostgresDataAccess[VolunteerProfileModel, VolunteerProfileInputSchema, VolunteerProfileSchema]
):
    _model = VolunteerProfileModel
    _input_schema = VolunteerProfileInputSchema
    _output_schema = VolunteerProfileSchema

    async def get_by_user_id(self, user_id: UUID) -> VolunteerProfileSchema:
        statement = select(self._model).where(self._model.user_id == user_id)

        if (model := (await self._session.scalar(statement))) is None:
            raise ObjectNotFound(f"The object with user_id={user_id} does not exist.")

        return self._output_schema.from_orm(model)

    def _apply_working_time_to_where_clause(self, statement, working_from: dt.time | None, working_to: dt.time | None):
        if working_from is not None:
            statement = statement.where(self._model.working_from >= working_from)

        if working_to is not None:
            statement = statement.where(self._model.working_to <= working_to)

        return statement

    def _apply_location_to_where_clause(self, statement, location: tuple[float, float], area_size: float):
        # check if database point (x2, y2) is inside circle (x, y) with radius area_size
        # sqrt((x2 - x)^2 + (y2 - y)^2) <= area_size
        x, y = location

        statement = statement.where(
            func.sqrt(func.pow(self._model.location_x - x, 2) + func.pow(self._model.location_y - y, 2)) <= area_size
        )
        return statement

    async def filter_by_params(
        self, params: VolunteerProfileFilterParams, limit: int = 50, offset: int = 0
    ) -> list[VolunteerProfileSchema]:
        params_dict = params.dict()

        profile_service_ids = (
            select(
                volunteer_profile_to_service.c.volunteer_profile_id,
                func.array_agg(volunteer_profile_to_service.c.volunteer_service_id, type_=pg.ARRAY(pg.UUID)).label(
                    "service_ids"
                ),
            )
            .group_by(volunteer_profile_to_service.c.volunteer_profile_id)
            .subquery()
        )

        statement = select(self._model, profile_service_ids.c.service_ids).join(
            profile_service_ids,
            VolunteerProfileModel.id == profile_service_ids.c.volunteer_profile_id,
            isouter=True,
        )

        statement = self._apply_working_time_to_where_clause(
            statement=statement, working_from=params_dict.pop("working_from"), working_to=params_dict.pop("working_to")
        )
        if (location := params_dict.pop("location")) is not None:
            statement = self._apply_location_to_where_clause(
                statement=statement, location=location, area_size=params_dict.pop("area_size")
            )

        services_ids = params_dict.pop("services_ids")

        statement = (
            statement.where(profile_service_ids.c.service_ids.contains([str(id_) for id_ in services_ids]))
            .where(and_(*(getattr(self._model, key) == value for key, value in params_dict.items())))
            .limit(limit)
            .offset(offset)
        )

        results = (await self._session.execute(statement)).all()
        print(results)

        return []
