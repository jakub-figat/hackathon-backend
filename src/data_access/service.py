from uuid import UUID

from src import VolunteerServiceModel
from src.data_access.base import BaseAsyncPostgresDataAccess
from src.exceptions.data_access import ObjectNotFound
from src.schemas.service.data_access import (
    VolunteerServiceInputSchema,
    VolunteerServiceSchema,
)


class VolunteerServiceDataAccess(
    BaseAsyncPostgresDataAccess[VolunteerServiceModel, VolunteerServiceInputSchema, VolunteerServiceSchema]
):
    _model = VolunteerServiceModel
    _input_schema = VolunteerServiceInputSchema
    _output_schema = VolunteerServiceSchema

    async def get_existing_services(self, services_ids: list[UUID]) -> list[VolunteerServiceSchema]:
        services = await self.get_many(limit=100)
        existing_services_ids = set(service.id for service in services)
        requested_services_ids = set(services_ids)
        if not requested_services_ids.issubset(existing_services_ids):
            ids_difference = [str(id_) for id_ in requested_services_ids - existing_services_ids]
            raise ObjectNotFound(f'Services with ids [{" ,".join(ids_difference)}] do not exist')

        return services
