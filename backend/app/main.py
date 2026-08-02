# app/main.py
from fastapi import FastAPI

from app.core.config import settings
from app.api.health import router as health_router

app = FastAPI(title=settings.app_name)

app.include_router(health_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root():
    return {"message": f"{settings.app_name} is running"}