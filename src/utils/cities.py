from itertools import chain

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import (
    TicketModel,
    VolunteerProfileModel,
)
from src.schemas.city import CitySchema


async def get_cities_from_profiles_and_tickets(session: AsyncSession) -> list[CitySchema]:
    ticket_cities = await session.scalars(select(TicketModel.city).distinct())
    profile_cities = await session.scalars(select(VolunteerProfileModel.city).distinct())
    return [CitySchema(name=city) for city in set(chain(ticket_cities, profile_cities))]
