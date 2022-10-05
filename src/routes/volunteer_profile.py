from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from src.deps.jwt import (
    get_request_user,
    require_auth,
)
from src.exceptions.data_access import ObjectNotFound
from src.schemas.user.dto import UserResponseSchema
from src.schemas.volunteer_profile.dto import (
    VolunteerProfileInputSchema,
    VolunteerProfileSchema,
)
from src.services.volunteer_profile import VolunteerProfileService


volunteer_profile_router = APIRouter(tags=["volunteer_profiles"])


@volunteer_profile_router.get(
    "/volunteers/",
    response_model=list[VolunteerProfileSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_auth)],
)
async def get_volunteer_profiles(
    volunteer_profile_service: VolunteerProfileService = Depends(),
) -> list[VolunteerProfileSchema]:
    return await volunteer_profile_service.get_profiles(limit=50, offset=50)  # TODO add paging


@volunteer_profile_router.get(
    "/volunteers/{profile_id}",
    response_model=VolunteerProfileSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_auth)],
)
async def get_volunteer_profile(
    profile_id: UUID,
    volunteer_profile_service: VolunteerProfileService = Depends(),
) -> VolunteerProfileSchema:
    try:
        return await volunteer_profile_service.get_profile(profile_id=profile_id)
    except ObjectNotFound:
        raise HTTPException(detail="Not found", status_code=status.HTTP_404_NOT_FOUND)


@volunteer_profile_router.post(
    "/volunteers/", response_model=VolunteerProfileSchema, status_code=status.HTTP_201_CREATED
)
async def create_volunteer_profile(
    schema: VolunteerProfileInputSchema,
    volunteer_profile_service: VolunteerProfileService = Depends(),
    user: UserResponseSchema = Depends(get_request_user),
) -> VolunteerProfileSchema:
    return await volunteer_profile_service.create_profile(schema=schema, user_id=user.id)


@volunteer_profile_router.put("/volunteers/", response_model=VolunteerProfileSchema, status_code=status.HTTP_200_OK)
async def create_volunteer_profile(
    schema: VolunteerProfileInputSchema,
    volunteer_profile_service: VolunteerProfileService = Depends(),
    user: UserResponseSchema = Depends(get_request_user),
) -> VolunteerProfileSchema:
    try:
        return await volunteer_profile_service.update_profile(schema=schema, user_id=user.id)
    except ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
