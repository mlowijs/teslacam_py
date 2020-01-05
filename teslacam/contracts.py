from abc import (ABC, abstractmethod)

from .models import Clip

class Uploader(ABC):
    @abstractmethod
    def can_upload(self) -> bool:
        pass

    @abstractmethod
    def upload(self, clip: Clip):
        pass