from fastapi import APIRouter
from status.service.status_service import check_all_services

router = APIRouter(prefix="/api/services")

@router.get("/health")
async def all_health():
    return await check_all_services()
