import time
import requests
from tqdm import tqdm

URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'


class Uploader:
	def __init__(self, session, photos: list, root_folder_name: str) -> None:
		self.photos_list = photos
		self.root_folder_name = root_folder_name
		self.session = session

	def _prepare_upload_params(self, photo, folder_type, folder_name: str) -> dict[str, str]:
		return {
			'url': photo['url'],
			'path': f'{self.root_folder_name}/{folder_type}/{folder_name}/{photo["filename"]}'
		}

	def _upload_photo(self, upload_params: dict[str, str]) -> None:
		try:
			upload = self.session.post(URL, params=upload_params)
			upload.raise_for_status()
		except requests.exceptions.HTTPError as e:
			print(f"Фото {upload_params['path']} не загружено: {e}")

	def upload_photos(self, folder_type, folder_name) -> None:
		for photo in tqdm(self.photos_list, desc="Загрузка фото на Яндекс Диск", unit="фото"):
			upload_params = self._prepare_upload_params(photo, folder_type, folder_name)
			self._upload_photo(upload_params)
			time.sleep(0.5)
		print(f'— Все {len(self.photos_list)} фото загружены')
