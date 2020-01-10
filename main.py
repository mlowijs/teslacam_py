from typing import List
import threading

from flask import Flask

from teslacam import config
from teslacam.consts import MIN_FILE_SIZE_BYTES, UPLOADERS
from teslacam.filesystem import FileSystem
from teslacam.funcs import group_by
from teslacam.models import Clip

cfg = config.load_config()
fs = FileSystem(cfg)
uploader = UPLOADERS[cfg.uploader](cfg)

def get_clips_to_upload(clips: List[Clip]) -> List[Clip]:
    to_upload: List[Clip] = []

    for event_clips in group_by(clips, lambda c: c.event).values():
        clips_by_date = group_by(event_clips, lambda c: c.date)
        dates = sorted(clips_by_date.keys())[-cfg.last_event_clips_count:]

        clips_to_upload = [clip for date in dates for clip in clips_by_date[date]]
        to_upload.extend([clip for clip in clips_to_upload if clip.size >= MIN_FILE_SIZE_BYTES])

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