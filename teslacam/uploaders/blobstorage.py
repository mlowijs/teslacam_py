from teslacam.config import Configuration
from azure.storage.blob import ContainerClient
from azure.core.exceptions import ServiceRequestError
from time import time

from teslacam.contracts import Uploader
from teslacam.models import Clip

class BlobStorageUploader(Uploader):
    def __init__(self, config: Configuration):
        super().__init__(config)

        blob_config = config["blobStorageUploader"]
        account_name = blob_config["accountName"]
        account_key = blob_config["accountKey"]
        container_name = blob_config["containerName"]

        self.__container_client = ContainerClient(f"https://{account_name}.blob.core.windows.net/",
            container_name, account_key, retry_total=1, connection_timeout=5)

    def can_upload(self) -> bool:
        try:
            props = self.__container_client.get_container_properties()
            return props != None
        except ServiceRequestError as err:
            return False

    def upload(self, clip: Clip):
        clip.date.strftime("")
        dir = f"{clip.date.year}/{clip.date.month}/{clip.date.day}" if clip.event != None else "recent"
        blob_name = f"{dir}/{clip.name}"

        blob_client = self.__container_client.get_blob_client(blob_name)

        with open(clip.path, "rb") as data:
            blob_client.upload_blob(data)