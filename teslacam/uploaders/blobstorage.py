from azure.storage.blob import BlobServiceClient

from ..contracts import Uploader
from ..models import Clip

class BlobStorageUploader(Uploader):
    def can_upload(self) -> bool:
        return True

    def upload(self, clip: Clip):
        pass