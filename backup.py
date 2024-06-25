import configparser
from modules.ya_disk_upload.ya_disk_uploader import YaDiskUploader
from modules.vk_modules.vk_api import VkProfilePhotosRetriever
from modules.create_json.create_json import create_json_file

config = configparser.ConfigParser()
config.read('settings.ini')
VK_TOKEN, YA_DISK_TOKEN = config['VK_API']['token'], config['YANDEX_DISK']['token']


class BackupPhotosFromVK:
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
	backup_photos_from_vk = BackupPhotosFromVK(
		VK_TOKEN, YA_DISK_TOKEN,
		133468233, 'profile', 22
	)
	backup_photos_from_vk.upload_from_disk()
	# backup_photos_from_vk.create_json()
