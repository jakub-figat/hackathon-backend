from enum import Enum


class TicketStatus(str, Enum):
    PENDING = "PENDING"
    CANCELED = "CANCELED"
    FINISHED = "FINISHED"
