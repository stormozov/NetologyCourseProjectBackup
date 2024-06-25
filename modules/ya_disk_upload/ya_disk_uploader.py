from modules.ya_disk_upload.folder_utils import FolderUtils
import requests


class YaDiskUploader:
    """YaDiskUploader class for uploading photos to Yandex Disk."""

    def __init__(self, token: str, photos: list, album_id: str) -> None:
        """
        Initializes the YaDiskUploader instance.

        Args:
            token: The OAuth token for authenticating with Yandex Disk API.
            photos: A list of photo objects to be uploaded.
            album_id: The ID of the album (e.g. "profile", "wall", "saved", "albums").
        """
        self.headers: dict[str, str] = {"Authorization": f'OAuth {token}'}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.photos_list: list = photos
        self.album_id = album_id

    def run(self) -> None:
        """
        Runs the upload process.

        Creates a FolderUtils instance and calls its create_folder_process method to create a
        folder structure and upload photos to Yandex Disk.
        """
        folder = FolderUtils(self.session, self.photos_list)
        folder.create_folder_process(self.album_id)
