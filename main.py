from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import router
from config.settings import settings


app = FastAPI(
    title="ConstructAI AI Service",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
