from abc import ABC, abstractmethod
from typing import Dict, Any


class StatusServiceInterface(ABC):
    """Contrato para servicios que exponen el estado de los componentes."""

    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual de todos los servicios."""
        pass
