from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)

from src.deps.jwt import (
    get_request_user,
    require_auth,
)
from src.exceptions.data_access import ObjectNotFound
from src.schemas.paging import (
    PaginatedResponseSchema,
    PagingInputParams,
)
from src.schemas.ticket.dto import (
    TicketFilterParams,
    TicketInputSchema,
    TicketQueryParams,
    TicketSchema,
)
from src.schemas.user.dto import UserResponseSchema
from src.services.ticket import TicketService


ticket_router = APIRouter(tags=["tickets"])


@ticket_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponseSchema[TicketSchema],
)
async def get_tickets(
    location: tuple[float, float] | None = Query(None),
    services_ids: list[UUID] = Query([]),
    ticket_params: TicketQueryParams = Depends(),
    paging_params: PagingInputParams = Depends(),
    ticket_service: TicketService = Depends(),
) -> PaginatedResponseSchema[TicketSchema]:
    ticket_filters = TicketFilterParams(**ticket_params.dict(), location=location, services_ids=services_ids)
    tickets = await ticket_service.get_tickets(*paging_params.to_limit_offset(), filter_params=ticket_filters)

    return PaginatedResponseSchema[TicketSchema].from_results(results=tickets, page_number=paging_params.page_number)


@ticket_router.get("/{ticket_id}/", status_code=status.HTTP_200_OK, response_model=TicketSchema)
async def get_ticket(ticket_id: UUID, ticket_service: TicketService = Depends()) -> TicketSchema:
    try:
        return await ticket_service.get_ticket(ticket_id=ticket_id)
    except ObjectNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@ticket_router.post("/", status_code=status.HTTP_201_CREATED, response_model=TicketSchema)
async def create_ticket(
    schema: TicketInputSchema,
    ticket_service: TicketService = Depends(),
    user: UserResponseSchema = Depends(get_request_user),
) -> TicketSchema:
    try:
        return await ticket_service.create_ticket(schema=schema, user_id=user.id)
    except ObjectNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@ticket_router.put("/{ticket_id}/", status_code=status.HTTP_200_OK, response_model=TicketSchema)
async def update_ticket(
    schema: TicketInputSchema,
    ticket_id: UUID,
    ticket_service: TicketService = Depends(),
    user: UserResponseSchema = Depends(get_request_user),
) -> TicketSchema:
    try:
        return await ticket_service.update_ticket(schema=schema, ticket_id=ticket_id, user_id=user.id)
    except ObjectNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@ticket_router.delete("/{ticket_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(
    ticket_id: UUID, ticket_service: TicketService = Depends(), user: UserResponseSchema = Depends(get_request_user)
) -> Response:
    try:
        await ticket_service.delete_ticket(ticket_id=ticket_id, user_id=user.id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ObjectNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
