from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from src.deps.jwt import get_verified_user
from src.exceptions.data_access import (
    ObjectAlreadyExists,
    ObjectNotFound,
)
from src.schemas.paging import (
    PaginatedResponseSchema,
    PagingInputParams,
)
from src.schemas.user.dto import UserResponseSchema
from src.schemas.volunteer_profile.dto import (
    VolunteerProfileFilterParams,
    VolunteerProfileInputSchema,
    VolunteerProfileQueryParams,
    VolunteerProfileSchema,
)
from src.services.volunteer_profile import VolunteerProfileService


volunteer_profile_router = APIRouter(tags=["volunteer_profiles"])


@volunteer_profile_router.get(
    "/",
    response_model=PaginatedResponseSchema[VolunteerProfileSchema],
    status_code=status.HTTP_200_OK,
)
async def get_volunteer_profiles(
    location: tuple[float, float] | None = Query(None),
    services_ids: list[UUID] = Query([]),
    profile_query_params: VolunteerProfileQueryParams = Depends(),
    paging_params: PagingInputParams = Depends(),
    volunteer_profile_service: VolunteerProfileService = Depends(),
) -> PaginatedResponseSchema[VolunteerProfileSchema]:
    profile_filter_params = VolunteerProfileFilterParams(
        **profile_query_params.dict(), location=location, services_ids=services_ids
    )
    profiles = await volunteer_profile_service.get_profiles(
        *paging_params.to_limit_offset(), filter_params=profile_filter_params
    )
    return PaginatedResponseSchema[VolunteerProfileSchema].from_results(
        results=profiles, page_number=paging_params.page_number
    )


@volunteer_profile_router.get(
    "/{profile_id}/",
    response_model=VolunteerProfileSchema,
    status_code=status.HTTP_200_OK,
)
async def get_volunteer_profile(
    profile_id: UUID,
    volunteer_profile_service: VolunteerProfileService = Depends(),
) -> VolunteerProfileSchema:
    try:
        return await volunteer_profile_service.get_profile(profile_id=profile_id)
    except ObjectNotFound:
        raise HTTPException(detail="Not found", status_code=status.HTTP_404_NOT_FOUND)


@volunteer_profile_router.post("/", response_model=VolunteerProfileSchema, status_code=status.HTTP_201_CREATED)
async def create_volunteer_profile(
    schema: VolunteerProfileInputSchema,
    volunteer_profile_service: VolunteerProfileService = Depends(),
    user: UserResponseSchema = Depends(get_verified_user),
) -> VolunteerProfileSchema:
    try:
        return await volunteer_profile_service.create_profile(schema=schema, user_id=user.id)
    except ObjectAlreadyExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Volunteer profile already exists")
    except ObjectNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@volunteer_profile_router.put("/", response_model=VolunteerProfileSchema, status_code=status.HTTP_200_OK)
async def update_volunteer_profile(
    schema: VolunteerProfileInputSchema,
    volunteer_profile_service: VolunteerProfileService = Depends(),
    user: UserResponseSchema = Depends(get_verified_user),
) -> VolunteerProfileSchema:
    try:
        return await volunteer_profile_service.update_profile(schema=schema, user_id=user.id)
    except ObjectNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
