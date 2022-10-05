from uuid import UUID

from fastapi import Depends

from src.data_access.volunteer_profile import VolunteerProfileDataAccess
from src.schemas.volunteer_profile import data_access
from src.schemas.volunteer_profile.dto import (
    VolunteerProfileInputSchema,
    VolunteerProfileSchema,
)


class VolunteerProfileService:
    def __init__(self, volunteer_profile_data_access: VolunteerProfileDataAccess = Depends()) -> None:
        self._volunteer_profile_data_access = volunteer_profile_data_access

    async def get_profile(self, profile_id: UUID) -> VolunteerProfileSchema:
        return VolunteerProfileSchema.from_orm(await self._volunteer_profile_data_access.get_by_id(id=profile_id))

    # TODO: more filter params
    async def get_profiles(self, limit: int, offset: int) -> list[VolunteerProfileSchema]:
        return [
            VolunteerProfileSchema.from_orm(profile)
            for profile in await self._volunteer_profile_data_access.get_many(limit=limit, offset=offset)
        ]

    async def create_profile(self, schema: VolunteerProfileInputSchema, user_id: UUID) -> VolunteerProfileSchema:
        return VolunteerProfileSchema.from_orm(
            await self._volunteer_profile_data_access.create(
                input_schema=data_access.VolunteerProfileInputSchema(**schema.dict(), user_id=user_id)
            )
        )

    async def update_profile(self, schema: VolunteerProfileInputSchema, user_id: UUID) -> VolunteerProfileSchema:
        profile_schema = await self._volunteer_profile_data_access.get_by_user_id(user_id=user_id)
        return VolunteerProfileSchema.from_orm(
            await self._volunteer_profile_data_access.update(
                update_schema=data_access.VolunteerProfileInputSchema.from_orm(schema), id=profile_schema.id
            )
        )
