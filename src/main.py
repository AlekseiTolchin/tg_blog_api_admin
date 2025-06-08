from fastapi import FastAPI

from src.api.posts import router as posts_router
from src.api.auth import router as auth_router


app = FastAPI()
app.include_router(posts_router)
app.include_router(auth_router)
