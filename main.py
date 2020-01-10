from flask import Flask

from teslacam import config
from teslacam.services import upload
from teslacam.services.filesystem import FileSystem

cfg = config.load_config()
fs = FileSystem(cfg)

# Start upload job
upload.start_job(cfg, fs)

# Setup web server
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"