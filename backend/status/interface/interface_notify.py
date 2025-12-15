from abc import ABC, abstractmethod


class NotifyInterface(ABC):
    """Contrato para el envío de notificaciones."""

    @abstractmethod
    async def send(self, message: str) -> None:
        """Envía un mensaje de notificación."""
        pass
