# TODO
# mounting filesystem
# select and discard x amount of clips per event
# run upload jobs in background
# notification

from typing import Dict, Mapping, Type
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

for type in config.clip_types:
    clips = fs.read_clips(type)

    for clip in clips:
        if uploader.can_upload():
            uploader.upload(clip)