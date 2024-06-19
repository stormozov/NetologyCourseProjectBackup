import yadisk


class YaDiskUploader:
	def __init__(self):
		self.headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			"Authorization": '',
		}
		self.folder_name = 'Бэкап фото из ВК'

	def upload_file(self, files: list):
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


test_url = [
	{
		'date': '2014-07-13',
		'likes': 33,
		'size_type': 'w',
		'url': 'https://sun9-78.userapi.com/impf/OWep7lGVPYkni13HGs2THchQrQI7NUVLkq2TMQ/UCbhU6kqW08.jpg?quality=96&as=32x53,48x80,72x120,108x180,160x267,240x401,360x601,480x802,540x902,640x1069,720x1203,1080x1804,1226x2048&sign=9c30648663ec06966fb9e1469ae03744&from=bu&cs=1226x2048'
	},
	{
		'date': '2016-05-09',
		'likes': 23,
		'size_type': 'z',
		'url': 'https://sun9-69.userapi.com/impf/c625318/v625318233/3a7d9/OdjNPFH6lX0.jpg?quality=96&as=32x57,48x85,72x128,108x192,160x284,240x426,360x638,480x851,540x958,609x1080&sign=9e5f88b04f0a6ed3d42d9a3da243346d&from=bu&cs=609x1080'
	}
]

ya_test = YaDiskUploader()
ya_test.upload_file(test_url)
