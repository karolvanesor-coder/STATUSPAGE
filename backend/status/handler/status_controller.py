from fastapi import APIRouter

from status.infra.status_repository_impl import StatusRepositoryImpl
from status.mapper.mapper_impl import StatusMapperImpl
from status.service.service_status import StatusServiceImpl

router = APIRouter(prefix="/api/services")

repo = StatusRepositoryImpl()
mapper = StatusMapperImpl()
service = StatusServiceImpl(repo, mapper)

@router.get("/health")
async def all_health():
    return await service.get_status()
