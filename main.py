# TODO
# mounting filesystem
# notification

from typing import Mapping, Type, List
import threading

from flask import Flask

from teslacam.uploaders.filesystem import FilesystemUploader
from teslacam.config import load_config
from teslacam.uploaders.blobstorage import BlobStorageUploader
from teslacam.contracts import Uploader
from teslacam.filesystem import Filesystem
from teslacam.models import Clip
from teslacam.funcs import group_by

UPLOADERS: Mapping[str, Type[Uploader]] = {
    "blobStorage": BlobStorageUploader,
    "filesystem": FilesystemUploader
}

config = load_config()

fs = Filesystem(config)
uploader = UPLOADERS[config.uploader](config)

def get_clips_to_upload(clips: List[Clip]) -> List[Clip]:
    to_upload: List[Clip] = []

    for event_clips in group_by(clips, lambda c: c.event).values():
        clips_by_date = group_by(event_clips, lambda c: c.date)
        keys = sorted(clips_by_date.keys())

        to_upload.extend([clip for date in keys[-config.last_event_clips_count:] for clip in clips_by_date[date]])

    return to_upload

def process_clips():
    for type in config.clip_types:
        print(f'Process clips of type {str(type)}')
        clips = fs.read_clips(type)

        for clip in get_clips_to_upload(clips):
            if uploader.can_upload():
                uploader.upload(clip)

        for clip in clips:
            clip.delete()
    
    threading.Timer(10, process_clips).start()

# Setup process timer
threading.Timer(5, process_clips).start()

# Setup web server
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"