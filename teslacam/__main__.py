from teslacam.services.upload import UploadService
from teslacam.log import log
from teslacam import config
from teslacam.services import upload
from teslacam.services.filesystem import FileSystem
from teslacam.services.notification import NotificationService

def main():
    cfg = config.load_config()
    
    fs = FileSystem(cfg)
    notification = NotificationService(cfg)

    upload = UploadService(cfg, fs, notification)

    # Start upload service
    upload.start()

    log("Started")

if __name__ == "__main__":
    main()