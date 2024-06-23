import requests

URL = 'https://cloud-api.yandex.net/v1/disk/resources'
ROOT_FOLDER_NAME = 'Бэкап фото из ВК'


class YaDiskUploader:
	def __init__(self, token: str, photos: list) -> None:
		self.headers: dict[str, str] = {"Authorization": f'OAuth {token}'}
		self.type_folder_name: str = ''
		self.photos_list: list = photos
		self.session = requests.Session()
		self.session.headers.update(self.headers)

	def create_folder_process(self, album_id: str) -> None:
		self._create_root_folder()
		self._create_type_folder(album_id)
		self._create_backup_folder(self.type_folder_name)

	def _create_root_folder(self):
		params: dict[str, str] = {'path': ROOT_FOLDER_NAME}
		response = self.session.get(URL, params=params)

		if response.status_code == 404:
			self.session.put(URL, params=params)
			print(f'Создана корневая папка резервных копий "{ROOT_FOLDER_NAME}"')

	def _create_type_folder(self, album_id: str):
		folder_mapping: dict[str, str] = {
			'profile': 'Фото профиля',
			'wall': 'Фото со стены',
			'saved': 'Сохраненные фото',
			'default': 'Альбом'
		}

		self.type_folder_name: str = folder_mapping.get(album_id, 'default')

		params = {'path': f'{ROOT_FOLDER_NAME}/{self.type_folder_name}'}

		try:
			response = self.session.get(URL, params=params)
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			if e.response.status_code == 404:
				self.session.put(URL, params=params)
				print(f'Создана папка "{folder_mapping.get(album_id, "default")}"')
			else:
				raise

	def _create_backup_folder(self, folder_type: str):
		root_folder_params: dict[str, str] = {'path': f'{ROOT_FOLDER_NAME}/{folder_type}'}
		create_folder_response = self.session.get(URL, params=root_folder_params)
		json_response = create_folder_response.json()['_embedded']['items']

		if not json_response:
			params = {'path': f'{ROOT_FOLDER_NAME}/{folder_type}/Резервная копия №1'}
			request = self.session.put(URL, params=params)
			if request.status_code == 201:
				print(f'Создана папка "Резервная копия №1"')
				self._upload_photos(folder_type, 'Резервная копия №1')
		else:
			count = 2
			while True:
				params = {'path': f'{ROOT_FOLDER_NAME}/{folder_type}/Резервная копия №{count}'}
				request = self.session.put(URL, params=params)

				if request.status_code == 201:
					print(f'Создана папка "Резервная копия №{count}"')
					break
				count += 1

			self._upload_photos(folder_type, f'Резервная копия №{count}')

	def _upload_photos(self, folder_type, folder_name: str):
		for idx, photo in enumerate(self.photos_list):
			upload_params: dict[str, str] = {
				'url': photo['url'],
				'path': f'{ROOT_FOLDER_NAME}/{folder_type}/{folder_name}/{photo['filename']}'
			}
			try:
				upload = self.session.post(f'{URL}/upload', params=upload_params)
				upload.raise_for_status()
				print(f"{idx + 1}. Фото {photo['filename']} загружено")
			except requests.exceptions.HTTPError as e:
				print(f"Фото {photo['filename']} не загружено: {e}")
		print(f'— Все {len(self.photos_list)} фото загружены')
