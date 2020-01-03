from pathlib import Path
from typing import List
from .enums import ClipType

class Clip:
    def __init__(self, path, type):
        self.__path = path
        self.__type = type

    @property
    def path(self) -> str:
        """
        Path to the clip file on the file system.
        """
        return self.__path

    @property
    def type(self) -> ClipType:
        """
        Type of the clip.
        """
        return self.__type

def read_clips(type: ClipType) -> List[Clip]:
    return []