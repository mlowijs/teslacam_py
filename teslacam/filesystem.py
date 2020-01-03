from typing import List
from pathlib import Path
from os import path

from .enums import ClipType
from .models import Clip
from .config import Configuration
from .consts import (TESLACAM_DIR)

class Filesystem:
    def __init__(self, config: Configuration):
        self.__config = config

    def read_clips(self, type: ClipType) -> List[Clip]:
        clip_dir = path.join(self.__config.tesla_cam_directory,
            TESLACAM_DIR)

        path = Path(clip_dir)
        return []