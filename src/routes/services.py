from fastapi import (
    APIRouter,
    Depends,
    status,
)

from src.data_access.service import VolunteerServiceDataAccess
from src.schemas.service.dto import VolunteerServiceSchema


service_router = APIRouter(tags=["services"])


@service_router.get("/", status_code=status.HTTP_200_OK, response_model=list[VolunteerServiceSchema])
async def get_volunteer_services(
    service_data_access: VolunteerServiceDataAccess = Depends(),
) -> list[VolunteerServiceSchema]:
    return [VolunteerServiceSchema.from_orm(service) for service in await service_data_access.get_many(limit=1000)]
