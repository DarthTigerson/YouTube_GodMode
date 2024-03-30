from fastapi import FastAPI
from routers import youtube
from starlette.staticfiles import StaticFiles

app = FastAPI(
    title="YouTube GodMode",
    description="Extra youtube options.",
    version="0.0.1",
    openapi_tags=[{
        "name": "youtube",
        "description": "Operations with YouTube videos",
    }]
)

app.include_router(youtube.router)
