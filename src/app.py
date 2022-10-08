from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.services import service_router
from src.routes.ticket import ticket_router
from src.routes.token import token_router
from src.routes.user import user_router
from src.routes.volunteer_profile import volunteer_profile_router
from src.settings import settings
from fastapi.staticfiles import StaticFiles


app = FastAPI()

if settings.debug:
    app.mount("/static", StaticFiles(directory="/var/www/media/"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=user_router, prefix="/users")
app.include_router(router=token_router, prefix="/token")
app.include_router(router=volunteer_profile_router, prefix="/volunteers")
app.include_router(router=ticket_router, prefix="/tickets")
app.include_router(router=service_router, prefix="/services")


# TODO: heading to ticket
# TODO: permissions with tickets
# TODO: volunteer rating and volunteer finished tickets
