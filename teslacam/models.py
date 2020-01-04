import re
from pathlib import Path
from datetime import datetime

from .enums import (ClipType, Camera)

DATE_REGEX = re.compile(r"^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})-")
CAMERA_REGEX = re.compile(r"-(\w+)\.mp4")

CAMERA_DICT = {
    "front": Camera.FRONT,
    "left_repeater": Camera.LEFT_REPEATER,
    "right_repeater": Camera.RIGHT_REPEATER,
    "back": Camera.BACK
}

class Clip:
    def __init__(self, path: Path, type: ClipType):
        self.__path = str(path)
        self.__type = type

        date = DATE_REGEX.findall(path.name)[0]
        self.__date = datetime.strptime(date, r"%Y-%m-%d_%H-%M-%S")

        camera = CAMERA_REGEX.findall(path.name)[0]
        self.__camera = CAMERA_DICT[camera]

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

    @property
    def date(self) -> datetime:
        """
        Date the clip was created.
        """
        return self.__date

    @property
    def camera(self) -> Camera:
        """
        Camera the clip was recorded with.
        """
        return self.__camera