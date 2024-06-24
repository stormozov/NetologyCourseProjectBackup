from modules.ya_disk_upload.upload_utils import Uploader
import requests

URL = 'https://cloud-api.yandex.net/v1/disk/resources'
ROOT_FOLDER_NAME = 'Бэкап фото из ВК'


class FolderUtils:
	def __init__(self, session, photos: list) -> None:
		self.photos_list = photos
		self.session = session

	def create_folder_process(self, album_id: str) -> None:
		self._create_folder(ROOT_FOLDER_NAME)

		type_folder_path = f'{ROOT_FOLDER_NAME}/{self._get_type_folder_name(album_id)}'
		self._create_folder(type_folder_path)

		backup_folder_path = self._get_backup_folder_name(type_folder_path)
		self._create_folder(backup_folder_path)

		backup_folder_name = backup_folder_path.split('/')[-1]  # Get the backup folder name
		self._upload(self._get_type_folder_name(album_id), backup_folder_name)

	def _upload(self, folder_type, folder_name: str) -> None:
		uploader = Uploader(self.session, self.photos_list, ROOT_FOLDER_NAME)
		uploader.upload_photos(folder_type, folder_name)

	@staticmethod
	def _get_type_folder_name(album_id: str) -> str:
		folder_mapping = {
			'profile': 'Фото профиля',
			'wall': 'Фото со стены',
			'saved': 'Сохраненные фото',
			'default': 'Альбом'
		}
		return folder_mapping.get(album_id, folder_mapping.get('default'))

	def _create_folder(self, path: str) -> None:
		params = {'path': path}
		try:
			response = self.session.get(URL, params=params)
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			if e.response.status_code == 404:
				self.session.put(URL, params=params)
				print(f'Создана папка "{path}"')
			else:
				raise

	def _get_backup_folder_name(self, type_folder_path: str) -> str:
		count = 1
		while True:
			backup_folder_path = f'{type_folder_path}/Резервная копия №{count}'
			try:
				response = self.session.get(URL, params={'path': backup_folder_path})
				response.raise_for_status()
			except requests.exceptions.HTTPError as e:
				if e.response.status_code == 404:
					self.session.put(URL, params={'path': backup_folder_path})
					print(f'Создана папка "Резервная копия №{count}"')
					return backup_folder_path
				else:
					raise
			count += 1
