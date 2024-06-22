import requests


class YaDiskUploader:
	def __init__(self, photos: list):
		self.headers = {
			"Authorization": '',
		}
		self.url = 'https://cloud-api.yandex.net/v1/disk/resources'
		self.root_folder_name = 'Бэкап фото из ВК'
		self.photos_list = photos
		self.date_format = '%d %B %Y'

	def create_folder_process(self):
		self._create_root_folder()
		self._create_folder()

	def _create_root_folder(self):
		params = {'path': self.root_folder_name}
		response = requests.get(self.url, headers=self.headers, params=params)

		if response.status_code == 404:
			requests.put(self.url, headers=self.headers, params=params)
			print(f'Создана корневая папка резервных копий "{self.root_folder_name}"')

	def _create_folder(self):
		root_folder_params = {'path': f'{self.root_folder_name}'}
		create_folder_response = requests.get(self.url, headers=self.headers, params=root_folder_params)
		json_response = create_folder_response.json()['_embedded']['items']

		if not json_response:
			params = {'path': f'{self.root_folder_name}/Резервная копия №1'}
			request = requests.put(self.url, headers=self.headers, params=params)
			if request.status_code == 201:
				print(f'Создана папка "Резервная копия №1"')
				self._upload_photos('Резервная копия №1')
		else:
			count = 2
			while True:
				params = {'path': f'{self.root_folder_name}/Резервная копия №{count}'}
				request = requests.put(self.url, headers=self.headers, params=params)

				if request.status_code == 201:
					print(f'Создана папка "Резервная копия №{count}"')
					break
				count += 1

			self._upload_photos(f'Резервная копия №{count}')

	def _upload_photos(self, folder_name: str):
		for idx, photo in enumerate(self.photos_list):
			upload_params = {
				'url': photo['url'],
				'path': f'{self.root_folder_name}/{folder_name}/{photo['filename']}'
			}
			upload = requests.post(f'{self.url}/upload', headers=self.headers, params=upload_params)
			if upload.status_code == 202:
				print(f'{idx + 1}. Фото "{photo["filename"]}" загружено')
			else:
				print(f'Фото "{photo["filename"]}" не загружено')
		print(f'— Все {len(self.photos_list)} фото загружены')
