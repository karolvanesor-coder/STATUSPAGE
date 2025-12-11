from abc import ABC, abstractmethod
from typing import Dict, Any


class StatusMapperInterface(ABC):
    """Interfaz para mapear y normalizar datos de servicios."""

    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convierte datos crudos de servicios en una estructura lista para el dominio.

        Args:
            raw_data (Dict[str, Any]): Datos sin procesar de los servicios.

        Returns:
            Dict[str, Any]: Datos normalizados y estandarizados.
        """
        pass
