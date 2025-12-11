from abc import ABC, abstractmethod
from typing import Dict, Any


class StatusServiceInterface(ABC):
    """Interfaz para servicios que proveen el estado de los componentes."""

    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual de los servicios.

        Returns:
            Dict[str, Any]: Estado de cada componente.
        """
        pass
