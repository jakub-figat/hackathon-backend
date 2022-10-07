from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.token import token_router
from src.routes.user import user_router
from src.routes.volunteer_profile import volunteer_profile_router
from src.settings import settings


app = FastAPI()

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

# TODO: service lookup and linking to volunteer profiles
