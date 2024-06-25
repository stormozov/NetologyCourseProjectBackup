import time
import requests
from tqdm import tqdm

URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'


class Uploader:
    """Uploader class for uploading photos to Yandex Disk."""

    def __init__(self, session, photos: list, root_folder_name: str) -> None:
        """
        Initializes the Uploader instance.

        Args:
            session: The session object for making requests to Yandex Disk API.
            photos: A list of photo objects to be uploaded.
            root_folder_name: The root folder name on Yandex Disk where photos will be uploaded.
        """
        self.photos_list = photos
        self.root_folder_name = root_folder_name
        self.session = session

    def _prepare_upload_params(self, photo, folder_type, folder_name: str) -> dict[str, str]:
        """
        Prepares the upload parameters for a single photo.

        Args:
            photo: A photo object to be uploaded.
            folder_type: The type of folder where the photo will be uploaded (e.g. "original", "thumb").
            folder_name: The name of the folder where the photo will be uploaded.

        Returns:
            A dictionary containing the upload parameters (url and path).
        """
        upload_photo_path: str = (f'{self.root_folder_name}/{folder_type}/{folder_name}'
                                  f'/{photo["filename"]}')
        return {'url': photo['url'], 'path': upload_photo_path}

    def _upload_photo(self, upload_params: dict[str, str]) -> None:
        """
        Uploads a single photo to Yandex Disk.

        Args:
            upload_params: A dictionary containing the upload parameters (url and path).

        Raises:
            requests.exceptions.HTTPError: If the upload fails.
        """
        try:
            upload = self.session.post(URL, params=upload_params)
            upload.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError(f'Фото {upload_params['path']} не загружено: {e}')

    def upload_photos(self, folder_type, folder_name) -> None:
        """
        Uploads all photos in the list to Yandex Disk.

        Args:
            folder_type: The type of folder where the photos will be uploaded (e.g. "original",
            "thumb").
            folder_name: The name of the folder where the photos will be uploaded.

        Returns:
            None
        """
        for photo in tqdm(self.photos_list, desc="Загрузка фото на Яндекс Диск", unit="фото"):
            upload_params = self._prepare_upload_params(photo, folder_type, folder_name)
            self._upload_photo(upload_params)
            time.sleep(0.5)
        print(f'— Все {len(self.photos_list)} фото загружены')
