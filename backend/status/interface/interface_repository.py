from abc import ABC, abstractmethod
from typing import Dict, Any

class StatusRepository(ABC):

    @abstractmethod
    async def get_services_status(self) -> Dict[str, Any]:
        """Return raw data of all services"""
        pass
