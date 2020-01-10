# TODO
# mounting filesystem
# notification

from typing import List
import threading

from flask import Flask

from teslacam import config
from teslacam.consts import UPLOADERS
from teslacam.filesystem import Filesystem
from teslacam.models import Clip
from teslacam.funcs import group_by

cfg = config.load_config()

fs = Filesystem(cfg)
uploader = UPLOADERS[cfg.uploader](cfg)

def get_clips_to_upload(clips: List[Clip]) -> List[Clip]:
    to_upload: List[Clip] = []

    for event_clips in group_by(clips, lambda c: c.event).values():
        clips_by_date = group_by(event_clips, lambda c: c.date)
        keys = sorted(clips_by_date.keys())

        to_upload.extend([clip for date in keys[-cfg.last_event_clips_count:] for clip in clips_by_date[date]])

    return to_upload

def process_clips():
    for type in cfg.clip_types:
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