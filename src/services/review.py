from uuid import UUID

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import (
    UserModel,
    VolunteerProfileModel,
)
from src.deps.db import get_async_session
from src.models.volunteer_review import VolunteerReviewModel
from src.schemas.review import ReviewInputSchema


class VolunteerReviewService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self._session = session

    async def add_review(self, schema: ReviewInputSchema, reviewer_id: UUID) -> None:
        if await self._session.scalar(select(UserModel).where(UserModel.id == reviewer_id)) is not None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reviewer not found")

        if (
            volunteer_profile := await self._session.scalar(
                select(VolunteerProfileModel).where(VolunteerProfileModel.id == schema.volunteer_profile_id)
            )
        ) is not None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volunteer profile not found")

        review = VolunteerReviewModel(
            reviewer_id=reviewer_id, volunteer_profile_id=volunteer_profile.id, rate=schema.rating, text=schema.text
        )
        self._session.add(review)
        await self._session.commit()
