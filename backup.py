import configparser
from modules.ya_disk_upload.ya_disk_uploader import YaDiskUploader
from modules.vk_modules.vk_api import VkProfilePhotosRetriever
from modules.create_json.create_json import create_json_file

config = configparser.ConfigParser()
config.read('settings.ini')
VK_TOKEN, YA_DISK_TOKEN = config['VK_API']['token'], config['YANDEX_DISK']['token']


class BackupPhotosFromVK:
	"""
	A class for backing up photos from a VK profile to Yandex Disk and creating a JSON file with
	the photo information.

	Attributes:
		- vk_token (str): The access token for the VK API.
		- ya_disk_token (str): The OAuth token for authenticating with Yandex Disk API.
		- user_id (int): The ID of the VK user whose photos are being backed up.
		- album_id (str | int): The ID of the album to retrieve photos from (default: 'profile').
		- count (int): The number of photos to retrieve (default: 5).
		- full_info (list): A list of dictionaries containing photo information.
		- json (dict): The original JSON response from the VK API.

	Methods:
		- upload_from_disk(): Uploads the photos to Yandex Disk.
		- create_json(): Creates a JSON file containing information about the backed up photos.
	"""
	def __init__(
			self, vk_token: str, ya_disk_token: str, user_id: int,
			album_id: str | int = 'profile', count: int = 5
	) -> None:
		data = VkProfilePhotosRetriever(
			vk_token, 'photos.get', user_id,
			album_id, count
		)
		self.ya_disk_token = ya_disk_token
		self.full_info = data.get_photos_info()['full_info']
		self.json = data.get_photos_info()['json']
		self.album_id = album_id

	def upload_from_disk(self) -> None:
		"""Uploads the photos to Yandex Disk."""
		ya_disk_uploader = YaDiskUploader(self.ya_disk_token, self.full_info, self.album_id)
		ya_disk_uploader.run()

	def create_json(self) -> None:
		"""Creates a JSON file containing information about the backed up photos."""
		create_json_file(self.json)


if __name__ == '__main__':
	ya_disk_token_entered = input('Введите ваш Yandex Disk token: ')
	user_id_entered = int(input('Введите ваш VK ID: '))
	album_id_entered = input('Введите альбом для загрузки (по умолчанию "profile"): ')
	count_entered = int(input('Количество фотографий для загрузки (по умолчанию 5): '))

	backup_photos_from_vk = BackupPhotosFromVK(
		VK_TOKEN, ya_disk_token_entered,
		user_id_entered, album_id_entered, count_entered
	)
	backup_photos_from_vk.upload_from_disk()
	# backup_photos_from_vk.create_json()
