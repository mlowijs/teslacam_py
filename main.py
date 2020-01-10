from teslacam import config
from teslacam.services import upload
from teslacam.services.filesystem import FileSystem

cfg = config.load_config()
fs = FileSystem(cfg)

# Start upload job
upload.start_job(cfg, fs)

# Start web server

