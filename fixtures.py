import asyncio
import datetime as dt

from sqlalchemy import insert

from src.db import Session
from src.models.services import VolunteerServiceModel
from src.models.ticket import (
    TicketModel,
    ticket_to_volunteer_service,
)
from src.models.user import UserModel
from src.models.volunteer_profile import VolunteerProfileModel


async def main() -> None:
    async with Session() as session:
        session.add_all(
            [
                UserModel(
                    email=f"stachu{num}@gmail.com",
                    password="$2b$12$0GbjzpKWAbS9k6f8ZJV.3O96B9nfLMIUyfJBkFbp/wTvEjCdS9lIy",  # hackathon
                    date_of_birth=dt.date(2000, 1, 1),
                    first_name="Stach",
                    last_name="Stach",
                )
                for num in range(1, 15)
            ]
        )
        session.add_all(
            [VolunteerServiceModel(name=name) for name in ["Pranie", "Sprzatanie", "Gotowanie", "Noszenie gruzu"]]
        )
        monster_delivery_service = VolunteerServiceModel(name="Monster delivery")
        session.add(monster_delivery_service)

        ticket_owner = UserModel(
            email="stachuowner@gmail.com",
            password="$2b$12$0GbjzpKWAbS9k6f8ZJV.3O96B9nfLMIUyfJBkFbp/wTvEjCdS9lIy",  # hackathon
            date_of_birth=dt.date(2000, 1, 1),
            first_name="Stach",
            last_name="Stach",
        )

        session.add(ticket_owner)
        await session.commit()

        session.add_all(
            [
                TicketModel(
                    location_x=1,
                    location_y=1,
                    city="Warsaw",
                    description="Bla bla bla",
                    valid_until=dt.datetime(2023, 1, 1),
                    user_id=ticket_owner.id,
                ),
                TicketModel(
                    location_x=2,
                    location_y=2,
                    city="Warsaw",
                    description="Bla bla bla",
                    valid_until=dt.datetime(2023, 1, 1),
                    user_id=ticket_owner.id,
                ),
                TicketModel(
                    location_x=3,
                    location_y=3,
                    city="Krakow",
                    description="Bla bla bla",
                    valid_until=dt.datetime(2023, 1, 1),
                    user_id=ticket_owner.id,
                ),
                TicketModel(
                    location_x=4,
                    location_y=4,
                    city="Krakow",
                    description="Bla bla bla",
                    valid_until=dt.datetime(2023, 1, 1),
                    user_id=ticket_owner.id,
                ),
                TicketModel(
                    location_x=5,
                    location_y=5,
                    city="Gliwice",
                    description="Bla bla bla",
                    valid_until=dt.datetime(2023, 1, 1),
                    user_id=ticket_owner.id,
                ),
            ]
        )
        await session.commit()

        ticket_with_services = TicketModel(
            location_x=6,
            location_y=6,
            city="Bilgoraj",
            description="Bla bla bla",
            valid_until=dt.datetime(2023, 1, 1),
            user_id=ticket_owner.id,
        )
        session.add(ticket_with_services)
        await session.commit()

        insert_ticket_service = insert(ticket_to_volunteer_service).values(
            (ticket_with_services.id, monster_delivery_service.id)
        )
        await session.execute(insert_ticket_service)
        await session.commit()

        profile_owner = UserModel(
            email="stachuprofileowner@gmail.com",
            password="$2b$12$0GbjzpKWAbS9k6f8ZJV.3O96B9nfLMIUyfJBkFbp/wTvEjCdS9lIy",  # hackathon
            date_of_birth=dt.date(2000, 1, 1),
            first_name="Stach",
            last_name="Stach",
        )
        session.add(profile_owner)
        await session.commit()

        session.add(
            VolunteerProfileModel(
                user_id=profile_owner.id,
                location_x=10,
                location_y=10,
                area_size=20,
                city="Jastrzebie-Zdroj",
                working_from=dt.time(12, 0),
                working_to=dt.time(20, 0),
            )
        )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
