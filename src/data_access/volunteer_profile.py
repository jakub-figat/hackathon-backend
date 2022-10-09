import datetime as dt
from typing import Iterable
from uuid import UUID

from sqlalchemy import (
    and_,
    delete,
    func,
    insert,
    select,
)
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import selectinload

from src import VolunteerProfileModel
from src.data_access.base import BaseAsyncPostgresDataAccess
from src.exceptions.data_access import ObjectNotFound
from src.models.volunteer_profile import volunteer_profile_to_service
from src.models.volunteer_review import VolunteerReviewModel
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

    async def get_by_id(self, id: UUID):
        statement = self._base_select.where(self._model.id == id)

        if (result := (await self._session.execute(statement)).first()) is None:
            raise ObjectNotFound(f"The object with id={id} does not exist.")

        return self._output_schema.with_rate(result[0], rate=result[1])

    async def get_by_user_id(self, user_id: UUID) -> VolunteerProfileSchema:
        statement = (
            select(self._model).options(selectinload(self._model.services)).where(self._model.user_id == user_id)
        )

        if (model := (await self._session.scalar(statement))) is None:
            raise ObjectNotFound(f"The object with user_id={user_id} does not exist.")

        return self._output_schema.from_orm(model)

    def _apply_working_time_to_where_clause(self, statement, working_from: dt.time | None, working_to: dt.time | None):
        if working_from is not None:
            statement = statement.where(self._model.working_from <= working_from)

        if working_to is not None:
            statement = statement.where(self._model.working_to >= working_to)

        return statement

    def _apply_location_to_where_clause(self, statement, location: tuple[float, float]):
        # check if database point (x2, y2) is inside circle (x, y) with radius area_size
        # sqrt((x2 - x)^2 + (y2 - y)^2) <= area_size
        x, y = location

        statement = statement.where(
            func.sqrt(func.pow(self._model.location_x - x, 2) + func.pow(self._model.location_y - y, 2))
            <= self._model.area_size
        )
        return statement

    async def filter_by_params(
        self, params: VolunteerProfileFilterParams, limit: int = 50, offset: int = 0
    ) -> list[VolunteerProfileSchema]:
        params_dict = params.dict()

        statement = self._base_select
        statement = self._apply_working_time_to_where_clause(
            statement=statement, working_from=params_dict.pop("working_from"), working_to=params_dict.pop("working_to")
        )

        if (location := params_dict.pop("location")) is not None:
            statement = self._apply_location_to_where_clause(statement=statement, location=location)

        if len(services_ids := params_dict.pop("services_ids")):
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

            statement = statement.join(
                profile_service_ids,
                VolunteerProfileModel.id == profile_service_ids.c.volunteer_profile_id,
                isouter=True,
            ).where(profile_service_ids.c.service_ids.contains([str(id_) for id_ in services_ids]))

        statement = (
            statement.where(
                and_(*(getattr(self._model, key) == value for key, value in params_dict.items() if value is not None))
            )
            .limit(limit)
            .offset(offset)
        )

        return [
            VolunteerProfileSchema.with_rate(profile, rate=rate)
            for profile, rate in await self._session.execute(statement)
        ]

    async def set_volunteer_services(self, profile_id: UUID, services_ids: Iterable[UUID]) -> None:
        await self.get_by_id(id=profile_id)
        await self._session.execute(delete(volunteer_profile_to_service))

        if services_ids:
            profiles_to_services = [(str(profile_id), str(service_id)) for service_id in services_ids]
            await self._session.execute(insert(volunteer_profile_to_service).values(profiles_to_services))
        await self._session.commit()

    @property
    def _aggregated_rates(self):
        table = VolunteerReviewModel.__table__
        return (
            select(table.c.volunteer_profile_id, func.coalesce(func.avg(table.c.rate), 0).label("rate"))
            .group_by(table.c.volunteer_profile_id)
            .subquery()
        )

    @property
    def _base_select(self):
        aggregates = self._aggregated_rates
        return (
            select(self._model, aggregates.c.rate)
            .options(selectinload(self._model.services))
            .join(aggregates, self._model.id == aggregates.c.volunteer_profile_id, isouter=True)
        )
