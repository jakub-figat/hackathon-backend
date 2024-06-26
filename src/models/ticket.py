from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    String,
    Table,
)
from sqlalchemy.orm import relationship

from src.db import Base
from src.enums.ticket import TicketStatus


ticket_to_volunteer_service = Table(
    "ticket_to_volunteer_service",
    Base.metadata,
    Column("ticket_id", ForeignKey("ticketmodels.id"), nullable=False),
    Column("volunteer_service_id", ForeignKey("volunteerservicemodels.id"), nullable=False),
)


class TicketModel(Base):
    title = Column(String(100), nullable=False)
    location_x = Column(Float, nullable=False)
    location_y = Column(Float, nullable=False)
    city = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    valid_until = Column(DateTime, nullable=False)
    user_id = Column(ForeignKey("usermodels.id"), nullable=False)
    status = Column(String(30), nullable=False, default=TicketStatus.PENDING.value)

    services = relationship("VolunteerServiceModel", secondary=ticket_to_volunteer_service, lazy="raise")
