import configparser
from modules.ya_disk_upload.ya_disk_uploader import YaDiskUploader
from modules.vk_modules.vk_api import VkProfilePhotosRetriever
from modules.create_json.create_json import create_json_file

config = configparser.ConfigParser()
config.read('settings.ini')
VK_TOKEN, YA_DISK_TOKEN = config['VK_API']['token'], config['YANDEX_DISK']['token']


class Backup:
	def __init__(
			self, vk_token: str, ya_disk_token: str,
			user_id: int, album_id: str = 'profile', count: int = 5
	) -> None:
		data = VkProfilePhotosRetriever(vk_token, 'photos.get', user_id, album_id, count)
		self.ya_disk_token = ya_disk_token
		self.full_info = data.get_photos_info()['full_info']
		self.json = data.get_photos_info()['json']

	def upload(self, album_id: str = 'profile') -> None:
		ya_disk_uploader = YaDiskUploader(self.ya_disk_token, self.full_info)
		ya_disk_uploader.create_folder_process(album_id)

	def create_json(self) -> None:
		create_json_file(self.json)


backup_photos_from_vk = Backup(
	VK_TOKEN, YA_DISK_TOKEN,
	133468233, 'profile', 12
)
backup_photos_from_vk.upload()
# backup_photos_from_vk.create_json()
