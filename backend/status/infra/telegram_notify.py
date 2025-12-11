import httpx
from status.interface.interface_notify import NotifyInterface


class TelegramNotify(NotifyInterface):

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    async def send(self, message: str):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message}

        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload)
