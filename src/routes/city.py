from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps.db import get_async_session
from src.schemas.city import CitySchema
from src.utils.cities import get_cities_from_profiles_and_tickets


city_router = APIRouter(tags=["cities"])


@city_router.get("/", response_model=list[CitySchema])
async def get_cities(session: AsyncSession = Depends(get_async_session)) -> list[CitySchema]:
    return await get_cities_from_profiles_and_tickets(session=session)
