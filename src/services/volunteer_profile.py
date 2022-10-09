from uuid import UUID

from fastapi import Depends

from src.data_access.service import VolunteerServiceDataAccess
from src.data_access.volunteer_profile import VolunteerProfileDataAccess
from src.schemas.volunteer_profile import data_access
from src.schemas.volunteer_profile.dto import (
    VolunteerProfileFilterParams,
    VolunteerProfileInputSchema,
    VolunteerProfileSchema,
)


class VolunteerProfileService:
    def __init__(
        self,
        volunteer_profile_data_access: VolunteerProfileDataAccess = Depends(),
        volunteer_service_data_access: VolunteerServiceDataAccess = Depends(),
    ) -> None:
        self._volunteer_profile_data_access = volunteer_profile_data_access
        self._volunteer_service_data_access = volunteer_service_data_access

    async def _set_profile_services(self, services_ids: list[UUID], profile: VolunteerProfileSchema) -> None:
        await self._volunteer_profile_data_access.set_volunteer_services(
            profile_id=profile.id, services_ids=services_ids
        )

    async def get_profile(self, profile_id: UUID) -> VolunteerProfileSchema:
        return VolunteerProfileSchema.from_orm(await self._volunteer_profile_data_access.get_by_id(id=profile_id))

    async def get_profiles(
        self, limit: int, offset: int, filter_params: VolunteerProfileFilterParams
    ) -> list[VolunteerProfileSchema]:
        profiles = await self._volunteer_profile_data_access.filter_by_params(
            params=filter_params, limit=limit, offset=offset
        )
        return [VolunteerProfileSchema.from_orm(profile) for profile in profiles]

    async def create_profile(self, schema: VolunteerProfileInputSchema, user_id: UUID) -> VolunteerProfileSchema:
        await self._volunteer_service_data_access.get_existing_services(services_ids=schema.services_ids)

        profile = await self._volunteer_profile_data_access.create(
            input_schema=data_access.VolunteerProfileInputSchema(**schema.dict(), user_id=user_id)
        )
        await self._set_profile_services(services_ids=schema.services_ids, profile=profile)

        return await self.get_profile(profile_id=profile.id)

    async def update_profile(self, schema: VolunteerProfileInputSchema, user_id: UUID) -> VolunteerProfileSchema:
        await self._volunteer_service_data_access.get_existing_services(services_ids=schema.services_ids)
        profile_schema = await self._volunteer_profile_data_access.get_by_user_id(user_id=user_id)
        profile = await self._volunteer_profile_data_access.update(
            update_schema=data_access.VolunteerProfileInputSchema(**schema.dict(), user_id=user_id),
            id=profile_schema.id,
        )
        await self._set_profile_services(services_ids=schema.services_ids, profile=profile_schema)

        return await self.get_profile(profile_id=profile.id)
