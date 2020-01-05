from abc import (ABC, abstractmethod)
from teslacam.config import Configuration

from teslacam.models import Clip

class Uploader(ABC):
    def __init__(self, config: Configuration):
        self.__config = config

    @abstractmethod
    def can_upload(self) -> bool:
        pass

    @abstractmethod
    def upload(self, clip: Clip):
        pass

    @property
    def config(self) -> Configuration:
        return self.__config