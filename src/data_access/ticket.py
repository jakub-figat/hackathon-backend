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

from src import TicketModel
from src.data_access.base import BaseAsyncPostgresDataAccess
from src.enums.ticket import TicketStatus
from src.models.ticket import ticket_to_volunteer_service
from src.schemas.ticket.data_access import (
    TicketInputSchema,
    TicketSchema,
)
from src.schemas.ticket.dto import TicketFilterParams


class TicketDataAccess(BaseAsyncPostgresDataAccess[TicketModel, TicketInputSchema, TicketSchema]):
    _model = TicketModel
    _input_schema = TicketInputSchema
    _output_schema = TicketSchema

    async def set_volunteer_services(self, ticket_id: UUID, services_ids: Iterable[UUID]) -> None:
        await self.get_by_id(id=ticket_id)
        await self._session.execute(delete(ticket_to_volunteer_service))

        if services_ids:
            profiles_to_services = [(str(ticket_id), str(service_id)) for service_id in services_ids]
            await self._session.execute(insert(ticket_to_volunteer_service).values(profiles_to_services))
        await self._session.commit()

    def _apply_valid_time_range_to_where_clause(self, statement, valid_from: dt.time | None, valid_to: dt.time | None):
        if valid_from is not None:
            statement = statement.where(self._model.valid_until >= valid_from)

        if valid_to is not None:
            statement = statement.where(self._model.valid_until <= valid_to)

        return statement

    def _apply_location_to_where_clause(self, statement, location: tuple[float, float], area_size: float):
        # check if ticket location belongs to circle (x, y) with radius area_size
        # sqrt((x2 - x)^2 + (y2 - y)^2) <= area_size
        x, y = location

        statement = statement.where(
            func.sqrt(func.pow(self._model.location_x - x, 2) + func.pow(self._model.location_y - y, 2)) <= area_size
        )
        return statement

    async def filter_by_params(
        self, filter_params: TicketFilterParams, limit: int = 50, offset: int = 0
    ) -> list[TicketSchema]:
        params_dict = filter_params.dict()

        statement = self._base_select
        statement = self._apply_valid_time_range_to_where_clause(
            statement=statement, valid_from=params_dict.pop("valid_from"), valid_to=params_dict.pop("valid_to")
        )

        area_size = params_dict.pop("area_size")
        if (location := params_dict.pop("location")) is not None:
            statement = self._apply_location_to_where_clause(
                statement=statement, location=location, area_size=area_size
            )

        if len(services_ids := params_dict.pop("services_ids")):
            ticket_service_ids = (
                select(
                    ticket_to_volunteer_service.c.ticket_id,
                    func.array_agg(ticket_to_volunteer_service.c.volunteer_service_id, type_=pg.ARRAY(pg.UUID)).label(
                        "service_ids"
                    ),
                )
                .group_by(ticket_to_volunteer_service.c.ticket_id)
                .subquery()
            )

            statement = statement.join(
                ticket_service_ids,
                TicketModel.id == ticket_service_ids.c.ticket_id,
                isouter=True,
            ).where(ticket_service_ids.c.service_ids.contains([str(id_) for id_ in services_ids]))

        statement = (
            statement.where(
                and_(*(getattr(self._model, key) == value for key, value in params_dict.items() if value is not None)),
                self._model.status == TicketStatus.PENDING.value,
            )
            .limit(limit)
            .offset(offset)
        )

        return [TicketSchema.from_orm(ticket) for ticket in await self._session.scalars(statement)]

    @property
    def _base_select(self):
        return super()._base_select.options(selectinload(self._model.services))
