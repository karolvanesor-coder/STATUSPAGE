from abc import ABC, abstractmethod
from typing import Dict, Any


class StatusRepository(ABC):
    """Interfaz para repositorios que proveen el estado de los servicios."""

    @abstractmethod
    async def get_services_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado de todos los servicios.

        Returns:
            Dict[str, Any]: Datos crudos de todos los servicios.
        """
        pass
