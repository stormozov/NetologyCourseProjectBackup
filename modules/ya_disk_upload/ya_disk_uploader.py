import requests


class YaDiskUploader:
	def __init__(self, photos: list):
		self.headers = {
			"Authorization": '',
		}
		self.url = 'https://cloud-api.yandex.net/v1/disk/resources'
		self.root_folder_name = 'Бэкап фото из ВК'
		self.type_folder_name = ''
		self.photos_list = photos
		self.session = requests.Session()
		self.session.headers.update(self.headers)

	def create_folder_process(self, album_id: str) -> None:
		self._create_root_folder()
		self._create_type_folder(album_id)
		self._create_backup_folder(self.type_folder_name)

	def _create_root_folder(self):
		params: dict[str, str] = {'path': self.root_folder_name}
		response = self.session.get(self.url, params=params)

		if response.status_code == 404:
			self.session.put(self.url, params=params)
			print(f'Создана корневая папка резервных копий "{self.root_folder_name}"')

	def _create_type_folder(self, album_id: str):
		folder_mapping = {
			'profile': 'Фото профиля',
			'wall': 'Фото со стены',
			'saved': 'Сохраненные фото',
			'default': 'Альбом'
		}

		self.type_folder_name = folder_mapping.get(album_id, 'default')

		params = {'path': f'{self.root_folder_name}/{self.type_folder_name}'}

		try:
			response = self.session.get(self.url, params=params)
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			if e.response.status_code == 404:
				self.session.put(self.url, params=params)
				print(f'Создана папка "{folder_mapping.get(album_id, "default")}"')
			else:
				raise

	def _create_backup_folder(self, folder_type: str):
		root_folder_params: dict[str, str] = {'path': f'{self.root_folder_name}/{folder_type}'}
		create_folder_response = self.session.get(self.url, params=root_folder_params)
		json_response = create_folder_response.json()['_embedded']['items']

		if not json_response:
			params = {'path': f'{self.root_folder_name}/{folder_type}/Резервная копия №1'}
			request = self.session.put(self.url, params=params)
			if request.status_code == 201:
				print(f'Создана папка "Резервная копия №1"')
				self._upload_photos(folder_type, 'Резервная копия №1')
		else:
			count = 2
			while True:
				params = {'path': f'{self.root_folder_name}/{folder_type}/Резервная копия №{count}'}
				request = self.session.put(self.url, params=params)

				if request.status_code == 201:
					print(f'Создана папка "Резервная копия №{count}"')
					break
				count += 1

			self._upload_photos(folder_type, f'Резервная копия №{count}')

	def _upload_photos(self, folder_type, folder_name: str):
		for idx, photo in enumerate(self.photos_list):
			upload_params: dict[str, str] = {
				'url': photo['url'],
				'path': f'{self.root_folder_name}/{folder_type}/{folder_name}/{photo['filename']}'
			}
			try:
				upload = self.session.post(f'{self.url}/upload', params=upload_params)
				upload.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
				print(f"{idx + 1}. Фото {photo['filename']} загружено")
			except requests.exceptions.HTTPError as e:
				print(f"Фото {photo['filename']} не загружено: {e}")
		print(f'— Все {len(self.photos_list)} фото загружены')
