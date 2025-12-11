from abc import ABC, abstractmethod

class NotifyInterface(ABC):

    @abstractmethod
    async def send(self, message: str):
        pass
