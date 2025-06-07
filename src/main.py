from fastapi import FastAPI

from src.api.posts import router as posts_router


app = FastAPI()
app.include_router(posts_router)
