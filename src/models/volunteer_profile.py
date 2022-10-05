from geoalchemy2 import Geography
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Time,
)
from sqlalchemy.orm import relationship

from src.db import Base


volunteer_profile_to_service = Table(
    "volunteer_profile_to_service",
    Base.metadata,
    Column("volunteer_profile_id", ForeignKey("volunteerprofilemodels.id"), nullable=False),
    Column("volunteer_service_id", ForeignKey("volunteerservicemodels.id"), nullable=False),
)


class VolunteerProfileModel(Base):
    location = Column(Geography("POINT"), nullable=False)
    area_size = Column(Integer, nullable=False)
    city = Column(String(100), nullable=False)
    working_from = Column(Time, nullable=False)
    working_to = Column(Time, nullable=False)

    services = relationship("VolunteerServiceModel", secondary=volunteer_profile_to_service, lazy="raise")
