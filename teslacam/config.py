from os import path
from typing import Any, List, Optional

import yaml

from teslacam.enums import ClipType

CONFIG_PATH = "/etc/teslacam.yml"

class Configuration:
    def __init__(self, config: dict):
        self.__tesla_cam_directory = config["teslaCamDirectory"]
        self.__mount_directory = config["mountDirectory"]
        self.__clip_types = [ClipType[type] for type in config["clipTypes"]]
        self.__last_event_clips_count = config["lastEventClipsCount"]
        self.__uploader = config["uploader"]
        
        self.__notifier = config.get("notifier")

        self.__dict = config

    def __getitem__(self, key: str) -> Any:
        return self.__dict[key]

    @property
    def tesla_cam_directory(self) -> str:
        """
        Directory containing the TeslaCam directory.
        """
        return self.__tesla_cam_directory

    @property
    def mount_directory(self) -> bool:
        """
        Indicates whether the tesla_cam_directory should be mounted.
        """
        return self.__mount_directory

    @property
    def last_event_clips_count(self) -> int:
        """
        The amount of latest clips that should be uploaded for every event.
        """
        return self.__last_event_clips_count

    @property
    def uploader(self) -> str:
        """
        The uploader to use.
        """
        return self.__uploader

    @property
    def clip_types(self) -> List[ClipType]:
        """
        Which clip types to upload.
        """
        return self.__clip_types

    @property
    def notifier(self) -> Optional[str]:
        """
        The notifier to use.
        """
        return self.__notifier

def load_config() -> Configuration:
    """
    Loads the application configuration from config.yml.
    """
    cfg_path = CONFIG_PATH if path.isfile(CONFIG_PATH) else "config.yml"

    with open(cfg_path) as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)
        print(cfg)
        return Configuration(cfg)