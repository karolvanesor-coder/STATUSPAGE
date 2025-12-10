from abc import ABC, abstractmethod
from typing import Dict, Any

class StatusServiceInterface(ABC):

    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        pass
