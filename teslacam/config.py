from typing import Any
import yaml

class Configuration:
    def __init__(self, config: dict):
        self.__tesla_cam_directory = config["teslaCamDirectory"]
        self.__mount_directory = config["mountDirectory"]
        self.__last_event_clips_count = config["lastEventClipsCount"]
        self.__uploader = config["uploader"]

        self.__dict = config

    def __getitem__(self, key: str) -> Any:
        return self.__dict[key]

    @property
    def tesla_cam_directory(self) -> str:
        return self.__tesla_cam_directory

    @property
    def mount_directory(self) -> bool:
        return self.__mount_directory

    @property
    def last_event_clips_count(self) -> int:
        return self.__last_event_clips_count

    @property
    def uploader(self) -> str:
        return self.__uploader

def load_config() -> Configuration:
    """
    Loads the application configuration from config.yml.
    """
    with open("config.yml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        return Configuration(config)