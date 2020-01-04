from typing import List
from pathlib import Path
from os import path

from .enums import ClipType
from .models import Clip
from .config import Configuration
from .consts import (TESLACAM_DIR, RECENT_DIR, SAVED_DIR, SENTRY_DIR)

class Filesystem:
    def __init__(self, config: Configuration):
        self.__config = config

    def read_clips(self, type: ClipType) -> List[Clip]:
        clips_dir = path.join(self.__config.tesla_cam_directory,
            TESLACAM_DIR, Filesystem.get_clip_dir(type))

        clips_path = Path(clips_dir)
        items = []
        
        for item in clips_path.iterdir():
            if item.is_file():
                items.append(Clip(item, type))

        return items

    @staticmethod
    def get_clip_dir(type: ClipType):
        if type == ClipType.RECENT:
            return RECENT_DIR
        elif type == ClipType.SAVED:
            return SAVED_DIR
        
        return SENTRY_DIR