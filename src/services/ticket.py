from uuid import UUID

from fastapi import Depends

from src.data_access.service import VolunteerServiceDataAccess
from src.data_access.ticket import TicketDataAccess
from src.schemas.ticket import data_access
from src.schemas.ticket.dto import (
    TicketFilterParams,
    TicketInputSchema,
    TicketSchema,
)


class TicketService:
    def __init__(
        self,
        ticket_data_access: TicketDataAccess = Depends(),
        volunteer_service_data_access: VolunteerServiceDataAccess = Depends(),
    ) -> None:
        self._ticket_data_access = ticket_data_access
        self._volunteer_service_data_access = volunteer_service_data_access

    async def get_ticket(self, ticket_id: UUID) -> TicketSchema:
        return TicketSchema.from_orm(await self._ticket_data_access.get_by_id(id=ticket_id))

    async def get_tickets(self, limit: int, offset: int, filter_params: TicketFilterParams) -> list[TicketSchema]:
        tickets = await self._ticket_data_access.filter_by_params(
            limit=limit, offset=offset, filter_params=filter_params
        )
        return [TicketSchema.from_orm(ticket) for ticket in tickets]

    async def create_ticket(self, schema: TicketInputSchema, user_id: UUID) -> TicketSchema:
        await self._volunteer_service_data_access.get_existing_services(services_ids=schema.services_ids)

        ticket = await self._ticket_data_access.create(
            input_schema=data_access.TicketInputSchema(**schema.dict(), user_id=user_id)
        )
        await self._set_ticket_services(services_ids=schema.services_ids, ticket=ticket)

        return await self.get_ticket(ticket_id=ticket.id)

    async def update_ticket(self, schema: TicketInputSchema, ticket_id: UUID, user_id: UUID) -> TicketSchema:
        await self._ticket_data_access.get_by(id=ticket_id, user_id=user_id)
        await self._volunteer_service_data_access.get_existing_services(services_ids=schema.services_ids)
        ticket = await self._ticket_data_access.update(
            update_schema=data_access.TicketInputSchema(**schema.dict(), user_id=user_id), id=ticket_id
        )

        await self._set_ticket_services(services_ids=schema.services_ids, ticket=ticket)
        return await self.get_ticket(ticket_id=ticket.id)

    async def _set_ticket_services(self, services_ids: list[UUID], ticket: TicketSchema) -> None:
        await self._ticket_data_access.set_volunteer_services(ticket_id=ticket.id, services_ids=services_ids)

    async def delete_ticket(self, ticket_id: UUID, user_id: UUID) -> None:
        ticket = await self._ticket_data_access.get_by(id=ticket_id, user_id=user_id)
        await self._set_ticket_services(services_ids=[], ticket=ticket)
        await self._ticket_data_access.delete_by_id(id=ticket_id)
