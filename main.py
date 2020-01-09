# TODO
# mounting filesystem
# select and discard x amount of clips per event
# notification

from typing import Dict, Mapping, Type, List, TypeVar, Callable, Any
import threading
from collections import defaultdict

from flask import Flask

from teslacam.uploaders.filesystem import FilesystemUploader
from teslacam.config import load_config
from teslacam.uploaders.blobstorage import BlobStorageUploader
from teslacam.contracts import Uploader
from teslacam.filesystem import Filesystem

UPLOADERS: Mapping[str, Type[Uploader]] = {
    "blobStorage": BlobStorageUploader,
    "filesystem": FilesystemUploader
}

config = load_config()

fs = Filesystem(config)
uploader = UPLOADERS[config.uploader](config)

TItem = TypeVar("TItem")
TKey = TypeVar("TKey")
def group_by(items: List[TItem], by: Callable[[TItem], TKey]) -> Dict[TKey, List[TItem]]:
    result: Dict[TKey, List[TItem]] = defaultdict(list)

    for item in items:
        result[by(item)].append(item)

    return result

def process_clips():
    for type in config.clip_types:
        print(f'Process clips of type {str(type)}')
        clips = fs.read_clips(type)

        # business logic
        date_grouped = group_by(clips, lambda c: c.event)
        filtered_groups = sorted(date_grouped.keys())[-config.last_event_clips_count:]

        for key in filtered_groups:
            pass

        # end business logic

        for clip in clips:
            if uploader.can_upload():
                uploader.upload(clip)
    
    threading.Timer(10, process_clips).start()

# Setup process timer
threading.Timer(10, process_clips).start()

# Setup web server
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"