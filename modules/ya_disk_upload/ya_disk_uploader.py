import requests


class YaDiskUploader:
	def __init__(self, photos: list):
		self.headers = {
			"Authorization": '',
		}
		self.folder_name = 'Бэкап фото из ВК'
		self.photos_list = photos

	def create_folder_process(self):
		url = 'https://cloud-api.yandex.net/v1/disk/resources'
		params = {'path': self.folder_name}
		response = requests.get(url, headers=self.headers, params=params)

		if response.status_code == 200:
			if self._delete_folder(url, params):
				if self._create_folder(url, params):
					print(f'Папка "{self.folder_name}" была создана повторно')
				else:
					print(f'Папка "{self.folder_name}" не была создана повторно')
			else:
				print(f'Папка "{self.folder_name}" уже создана')
		else:
			print(f'Папки "{self.folder_name}" нет на диске')
			if self._create_folder(url, params):
				print(f'Папка "{self.folder_name}" была создана')
			else:
				print(f'Папка "{self.folder_name}" не была создана')

	def _delete_folder(self, url, params):
		response = requests.delete(url, headers=self.headers, params=params)
		return response.status_code == 204

	def _create_folder(self, url, params):
		response = requests.put(url, headers=self.headers, params=params)
		return response.status_code == 201

	def _upload_photos(self):
		url2 = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
		for photo in self.photos_list:
			upload_params = {
				'url': photo['url'],
				'path': f'{self.folder_name}/{photo["filename"]}'
			}
			upload = requests.post(url2, headers=self.headers, params=upload_params)
			if upload.status_code == 202:
				print(f'Фото {photo["filename"]} загружено')
			else:
				print(f'Фото {photo["filename"]} не загружено')
		print(f'— Все {len(self.photos_list)} фото загружены')
