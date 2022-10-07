from uuid import UUID

from fastapi import Depends

from src.data_access.volunteer_profile import VolunteerProfileDataAccess
from src.schemas.volunteer_profile import data_access
from src.schemas.volunteer_profile.dto import (
    VolunteerProfileFilterParams,
    VolunteerProfileInputSchema,
    VolunteerProfileSchema,
)


class VolunteerProfileService:
    def __init__(self, volunteer_profile_data_access: VolunteerProfileDataAccess = Depends()) -> None:
        self._volunteer_profile_data_access = volunteer_profile_data_access

    async def get_profile(self, profile_id: UUID) -> VolunteerProfileSchema:
        return VolunteerProfileSchema.from_orm(await self._volunteer_profile_data_access.get_by_id(id=profile_id))

    async def get_profiles(
        self, limit: int, offset: int, filter_params: VolunteerProfileFilterParams | None = None
    ) -> list[VolunteerProfileSchema]:
        profiles = await (
            self._volunteer_profile_data_access.get_many(limit=limit, offset=offset)
            if filter_params is None
            else self._volunteer_profile_data_access.filter_by_params(params=filter_params, limit=limit, offset=offset)
        )
        return [VolunteerProfileSchema.from_orm(profile) for profile in profiles]

    async def create_profile(self, schema: VolunteerProfileInputSchema, user_id: UUID) -> VolunteerProfileSchema:
        profile = await self._volunteer_profile_data_access.create(
            input_schema=data_access.VolunteerProfileInputSchema(**schema.dict(), user_id=user_id)
        )
        location = profile.location_x, profile.location_y
        return VolunteerProfileSchema(**profile.dict(exclude={"location_x", "location_y"}), location=location)

    async def update_profile(self, schema: VolunteerProfileInputSchema, user_id: UUID) -> VolunteerProfileSchema:
        profile_schema = await self._volunteer_profile_data_access.get_by_user_id(user_id=user_id)
        return VolunteerProfileSchema.from_orm(
            await self._volunteer_profile_data_access.update(
                update_schema=data_access.VolunteerProfileInputSchema.from_orm(schema), id=profile_schema.id
            )
        )
