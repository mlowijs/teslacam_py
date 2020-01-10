from typing import Mapping, Type

from teslacam.contracts import Uploader
from teslacam.uploaders.blobstorage import BlobStorageUploader
from teslacam.uploaders.filesystem import FilesystemUploader

UPLOADERS: Mapping[str, Type[Uploader]] = {
    "blobStorage": BlobStorageUploader,
    "filesystem": FilesystemUploader
}

TESLACAM_DIR = "TeslaCam"

RECENT_DIR = "RecentClips"
SAVED_DIR = "SavedClips"
SENTRY_DIR = "SentryClips"