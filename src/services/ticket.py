from uuid import UUID

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import (
    and_,
    select,
)
from sqlalchemy.orm import selectinload

from src import TicketModel
from src.data_access.service import VolunteerServiceDataAccess
from src.data_access.ticket import TicketDataAccess
from src.enums.ticket import TicketStatus
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
        session = self._ticket_data_access._session

        ticket = await session.scalar(
            select(TicketModel)
            .options(selectinload)
            .where(and_(TicketModel.id == ticket_id, TicketModel.status == TicketStatus.PENDING.value))
        )
        if ticket is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

        return TicketSchema.from_orm(ticket)

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
        await self._ticket_data_access.get_by(id=ticket_id, user_id=user_id, status=TicketStatus.PENDING.value)
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

    async def cancel_ticket(self, ticket_id: UUID, user_id: UUID) -> None:
        session = self._ticket_data_access._session
        ticket = await session.scalar(
            select(TicketModel).where(
                and_(
                    TicketModel.id == ticket_id,
                    TicketModel.user_id == user_id,
                    TicketModel.status == TicketStatus.PENDING.value,
                )
            )
        )
        if ticket is None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Ticket not found")

        ticket.status = TicketStatus.CANCELED.value
        session.add(ticket)
        await session.commit()

    async def finish_ticket(self, ticket_id: UUID, user_id: UUID) -> None:
        session = self._ticket_data_access._session
        ticket = await session.scalar(
            select(TicketModel).where(
                and_(
                    TicketModel.id == ticket_id,
                    TicketModel.user_id == user_id,
                    TicketModel.status == TicketStatus.PENDING.value,
                )
            )
        )

        if ticket is None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Ticket not found")

        ticket.status = TicketStatus.FINISHED.value
        session.add(ticket)
        await session.commit()
