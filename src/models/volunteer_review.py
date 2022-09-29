from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)

from src.db import Base


class VolunteerReviewModel(Base):
    reviewer_id = Column(ForeignKey("usermodels.id"), nullable=False)
    volunteer_profile_id = Column(ForeignKey("volunteerprofilemodels.id"), nullable=False)
    rate = Column(Integer, nullable=False)
    text = Column(String(100), nullable=False)
