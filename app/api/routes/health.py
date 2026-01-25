from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("/health", summary="Service health")
async def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }
