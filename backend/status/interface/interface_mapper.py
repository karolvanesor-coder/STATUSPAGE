from abc import ABC, abstractmethod
from typing import Any, Dict


class StatusMapperInterface(ABC):
    """Contrato para normalizar el estado de los servicios."""

    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliza los datos crudos y calcula el estado general."""
        pass
