from threading import Timer
from typing import List

from teslacam.config import Configuration
from teslacam.consts import MIN_FILE_SIZE_BYTES, UPLOADERS
from teslacam.funcs import group_by
from teslacam.models import Clip
from teslacam.services.filesystem import FileSystem

UPLOAD_INTERVAL = 30

def start_job(cfg: Configuration, fs: FileSystem):
    Timer(UPLOAD_INTERVAL, __process_clips, [cfg, fs]).start()    

def __process_clips(cfg: Configuration, fs: FileSystem):
    uploader = UPLOADERS[cfg.uploader](cfg)

    if (cfg.mount_directory):
        fs.mount_directory()

    for type in cfg.clip_types:
        print(f"Process clips of type {str(type)}")
        clips = fs.read_clips(type)

        for clip in __get_clips_to_upload(clips, cfg):
            print(f"Uploading clip '{clip.name}'")
            if uploader.can_upload():
                uploader.upload(clip)

        for clip in clips:
            print(f"Deleting clip '{clip.name}'")
            clip.delete()

    if (cfg.mount_directory):
        fs.unmount_directory()
    
    print("Processing complete")
    start_job(cfg, fs)

def __get_clips_to_upload(clips: List[Clip], cfg: Configuration) -> List[Clip]:
    to_upload: List[Clip] = []

    for event_clips in group_by(clips, lambda c: c.event).values():
        clips_by_date = group_by(event_clips, lambda c: c.date)
        dates = sorted(clips_by_date.keys())[-cfg.last_event_clips_count:]

        clips_to_upload = [clip
            for date in dates
            for clip in clips_by_date[date]
            if clip.size >= MIN_FILE_SIZE_BYTES]

        to_upload.extend(clips_to_upload)

    return to_upload