import yadisk


class YaDiskUploader:
	def __init__(self, photos: list):
		self.headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			"Authorization": '',
		}
		self.folder_name = 'Бэкап фото из ВК'
		self.photos_list = photos

	def upload_file(self):
		files = self.photos_list
		client = yadisk.Client(token=self.headers['Authorization'])
		if client.check_token():
			if not client.is_dir(self.folder_name):
				client.mkdir(self.folder_name)
				print('Folder created successfully.')

			for file in files:
				file_name = file['likes']
				file_url = file['url']
				client.upload_url(file_url, f'{self.folder_name}/{file_name}.jpg')
				print(f'File "{file_name}.jpg" uploaded successfully.')

			print(f'{len(files)} files uploaded successfully.')
		else:
			print('Token is invalid.')
