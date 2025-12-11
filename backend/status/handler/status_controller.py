from fastapi import APIRouter

router = APIRouter(prefix="/api/services")

service = None  # será inyectado desde main.py


@router.get("/health")
async def all_health():
    return await service.get_status()
