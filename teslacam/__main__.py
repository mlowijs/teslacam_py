from teslacam import config
from teslacam.services import upload
from teslacam.services.filesystem import FileSystem

def main():
    cfg = config.load_config()
    fs = FileSystem(cfg)

    # Start upload job
    upload.start_job(cfg, fs)

    # Start web server

    print("Started")

if __name__ == "__main__":
    main()