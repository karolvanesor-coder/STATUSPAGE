from fastapi import APIRouter
from typing import Any

router = APIRouter(prefix="/api/services")

service: Any = None  

@router.get("/health")
async def all_health():
    """Devuelve el estado de todos los servicios."""
    return await service.get_status()
