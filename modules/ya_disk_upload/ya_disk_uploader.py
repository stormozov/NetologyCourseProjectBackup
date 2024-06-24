from modules.ya_disk_upload.folder_utils import FolderUtils
import requests


class YaDiskUploader:
	def __init__(self, token: str, photos: list, album_id: str) -> None:
		self.headers: dict[str, str] = {"Authorization": f'OAuth {token}'}
		self.session = requests.Session()
		self.session.headers.update(self.headers)
		self.photos_list: list = photos
		self.album_id = album_id

	def run(self):
		folder = FolderUtils(self.session, self.photos_list)
		folder.create_folder_process(self.album_id)
