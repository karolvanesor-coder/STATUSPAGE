from datetime import datetime
from status.interface.interface_service import StatusServiceInterface
from status.interface.interface_repository import StatusRepository
from status.interface.interface_mapper import StatusMapperInterface


class StatusServiceImpl(StatusServiceInterface):

    def __init__(self, repo: StatusRepository, mapper: StatusMapperInterface):
        self.repo = repo
        self.mapper = mapper

    async def get_status(self):
        raw = await self.repo.get_services_status()
        normalized = self.mapper.normalize(raw)

        normalized["timestamp"] = datetime.utcnow().isoformat() + "Z"

        return normalized
