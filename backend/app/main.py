# app/main.py
from fastapi import FastAPI

from app.core.config import settings
from app.api.health import router as health_router
from app.api.news import router as news_router

from fastapi.middleware.cors import CORSMiddleware 

from fastapi.staticfiles import StaticFiles
import os


app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.api_v1_prefix)
app.include_router(news_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root():
    return {"message": f"{settings.app_name} is running"}

os.makedirs("media/uploads", exist_ok=True)
app.mount("/media", StaticFiles(directory="media"), name="media")