from abc import ABC, abstractmethod
from typing import Dict, Any

class StatusMapperInterface(ABC):

    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert raw services data into domain-ready structure"""
        pass
