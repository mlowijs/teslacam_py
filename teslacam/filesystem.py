from typing import List
from pathlib import Path
from os import path
from sh import mount, umount

from teslacam.enums import ClipType
from teslacam.models import Clip
from teslacam.config import Configuration
from teslacam.consts import TESLACAM_DIR, RECENT_DIR, SAVED_DIR, SENTRY_DIR

class Filesystem:
    def __init__(self, config: Configuration):
        self.__config = config

    def read_clips(self, type: ClipType) -> List[Clip]:
        if (self.__config.mount_directory):
            self.mount_directory()

        clips_dir = path.join(self.__config.tesla_cam_directory,
            TESLACAM_DIR, Filesystem.__get_clip_dir(type))

        clips_path = Path(clips_dir)

        if not clips_path.exists():
            return []

        clips = Filesystem.__get_items(clips_path, type)

        if (self.__config.mount_directory):
            self.unmount_directory()

        return clips

    def mount_directory(self):
        mount(self.__config.tesla_cam_directory)

    def unmount_directory(self):
        umount(self.__config.tesla_cam_directory)

    @staticmethod
    def __get_items(clips_path: Path, type: ClipType, items: List[Clip]=None, event: str=None) -> List[Clip]:
        items = [] if items == None else items

        for item in clips_path.iterdir():
            if item.is_file() and path.splitext(item.name)[1] == ".mp4":
                items.append(Clip(item, type, event))
            
            if item.is_dir():
                Filesystem.__get_items(item, type, items, item.name)

        return items

    @staticmethod
    def __get_clip_dir(type: ClipType):
        if type == ClipType.RECENT:
            return RECENT_DIR
        elif type == ClipType.SAVED:
            return SAVED_DIR
        
        return SENTRY_DIR