from abc import ABC, abstractmethod
from typing import Dict, Any


class StatusRepository(ABC):
    """Contrato para repositorios que consultan el estado de los servicios."""

    @abstractmethod
    async def get_services_status(self) -> Dict[str, Any]:
        """Obtiene el estado crudo de todos los servicios."""
        pass
