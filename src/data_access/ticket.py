from src import TicketModel
from src.data_access.base import BaseAsyncPostgresDataAccess
from src.schemas.ticket.data_access import (
    TicketInputSchema,
    TicketSchema,
)


class TicketDataAccess(BaseAsyncPostgresDataAccess[TicketModel, TicketInputSchema, TicketSchema]):
    _model = TicketModel
    _input_schema = TicketInputSchema
    _output_schema = TicketSchema
