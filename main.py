# TODO
# uploader to blob storage
# mounting filesystem
# select and discard x amount of clips per event
# run upload jobs in background
# notification

from typing import Dict, Mapping, Type
from teslacam.uploaders.filesystem import FilesystemUploader
from teslacam.config import (load_config, Configuration)
from teslacam.uploaders.blobstorage import BlobStorageUploader
from teslacam.contracts import Uploader
from teslacam.enums import ClipType
from teslacam.filesystem import Filesystem

UPLOADERS: Mapping[str, Type[Uploader]] = {
    "blobStorage": BlobStorageUploader,
    "filesystem": FilesystemUploader
}

def get_uploader(config: Configuration) -> Uploader:
    return UPLOADERS[config.uploader](config)

config = load_config()

fs = Filesystem(config)
uploader = get_uploader(config)

for type in [ClipType.SAVED, ClipType.SENTRY]:
    clips = fs.read_clips(type)

    for clip in clips:
        if uploader.can_upload():
            uploader.upload(clip)