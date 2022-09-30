from fastapi import FastAPI

from src.routes.user import user_router


app = FastAPI()
app.include_router(router=user_router, prefix="/users")
