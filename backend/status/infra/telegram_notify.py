import httpx
from status.interface.interface_notify import NotifyInterface


class TelegramNotify(NotifyInterface):
    """Notificador para enviar mensajes vía Telegram."""

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    async def send(self, message: str) -> None:
        """
        Envía un mensaje al chat de Telegram configurado.
        
        """
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message}

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            # El servidor respondió con un status code 4xx o 5xx
            print(f"Error al enviar mensaje a Telegram: {exc.response.status_code}")
        except httpx.RequestError as exc:
            # Error de conexión o timeout
            print(f"Error de conexión al enviar mensaje a Telegram: {exc}")
