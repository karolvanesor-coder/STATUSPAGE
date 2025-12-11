from abc import ABC, abstractmethod


class NotifyInterface(ABC):
    """Interfaz para notificaciones de servicios."""

    @abstractmethod
    async def send(self, message: str) -> None:
        """
        Envía un mensaje de notificación.

        Args:
            message (str): El mensaje a enviar.
        """
        pass
