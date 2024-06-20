import configparser
from modules.fetch_photos_info.fetch_photos_info import fetch_photo_data
from modules.vk_modules.vk_photo_processor import VKPhotoProcessor
from modules.create_json.create_json import create_json_file


class VkProfilePhotosRetriever(VKPhotoProcessor):
	config = configparser.ConfigParser()
	config.read('settings.ini')
	vk_api = config['VK_API']
	API_VERSION: int = vk_api['Api_version']
	URL: str = vk_api['Url']
	TOKEN: str = vk_api['Token']
	DATE_FORMAT: str = '%Y-%m-%d'
	PREFERRED_SIZES = ['w', 'z']

	def __init__(self, method: str, user_id: int, album_id: str = 'wall', count: int = 5) -> None:
		self.method = method
		self.params = {
			'access_token': self.TOKEN,
			'owner_id': user_id,
			'album_id': album_id,
			'count': count,
			'extended': 1,
			'photo_sizes': 1,
			'v': self.API_VERSION,
		}
		self.extracted_photo_info: dict[str, list] = {}

	def get_photos_info(self):
		data = fetch_photo_data(self.URL, self.method, self.params)
		if 'response' in data and 'items' in data['response']:
			photos = data['response']['items']
			self.extracted_photo_info = self._extract_photo_info(
				photos, self.DATE_FORMAT, self.PREFERRED_SIZES
			)
			return self.extracted_photo_info['full_info']
		else:
			return []


test = VkProfilePhotosRetriever('photos.get', 133468233, 'profile', 12)
result = test.get_photos_info()
