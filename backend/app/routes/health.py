from fastapi import APIRouter

from app.services.health_service import get_health_status, insert_test_document

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    return get_health_status()


