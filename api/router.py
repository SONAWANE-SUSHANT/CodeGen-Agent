from fastapi import APIRouter

from config.settings import settings


router = APIRouter()


@router.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.app_env,
    }
