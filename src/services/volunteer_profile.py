from uuid import UUID

from fastapi import Depends

from src.data_access.service import VolunteerServiceDataAccess
from src.data_access.volunteer_profile import VolunteerProfileDataAccess
from src.exceptions.data_access import ObjectNotFound
from src.schemas.service.dto import VolunteerServiceSchema
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

    async def _set_profile_services(
        self, schema: VolunteerProfileInputSchema, profile: VolunteerProfileSchema
    ) -> list[VolunteerServiceSchema]:
        services = await self._volunteer_service_data_access.get_many(limit=100)
        services_ids = set(service.id for service in services)
        schema_services_ids = set(schema.services_ids)
        if not schema_services_ids.issubset(services_ids):
            ids_difference = [str(id_) for id_ in schema_services_ids - services_ids]
            raise ObjectNotFound(f'Services with ids [{" ,".join(ids_difference)}] do not exist')

        await self._volunteer_profile_data_access.set_volunteer_services(
            profile_id=profile.id, services_ids=services_ids
        )

        return [VolunteerServiceSchema.from_orm(service) for service in services if service.id in schema_services_ids]

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
        profile = await self._volunteer_profile_data_access.create(
            input_schema=data_access.VolunteerProfileInputSchema(**schema.dict(), user_id=user_id)
        )
        services = await self._set_profile_services(schema=schema, profile=profile)

        return VolunteerProfileSchema.from_orm(profile, services=services)

    async def update_profile(self, schema: VolunteerProfileInputSchema, user_id: UUID) -> VolunteerProfileSchema:
        profile_schema = await self._volunteer_profile_data_access.get_by_user_id(user_id=user_id)
        services = await self._set_profile_services(schema=schema, profile=profile_schema)

        return VolunteerProfileSchema.from_orm(
            await self._volunteer_profile_data_access.update(
                update_schema=data_access.VolunteerProfileInputSchema(**schema.dict(), user_id=user_id),
                id=profile_schema.id,
            ),
            services=services,
        )
