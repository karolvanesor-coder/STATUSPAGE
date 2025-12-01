from fastapi import APIRouter
from app.services.services_manager import check_all_services

router = APIRouter(prefix="/api/services")

@router.get("/health")
async def all_health():
    return await check_all_services()
