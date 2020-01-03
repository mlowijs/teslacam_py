import yaml

class Configuration:
    def __init__(self, config: dict):
        self.__tesla_cam_directory = config['teslaCamDirectory']
        self.__mount_directory = config['mountDirectory']
        self.__last_event_clips_count = config['lastEventClipsCount']        

    @property
    def tesla_cam_directory(self) -> str:
        return self.__tesla_cam_directory

    @property
    def mount_directory(self) -> bool:
        return self.__mount_directory

    @property
    def last_event_clips_count(self) -> int:
        return self.__last_event_clips_count

def load() -> Configuration:
    """
    Loads the application configuration from config.yml.
    """
    with open("config.yml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        return Configuration(config)