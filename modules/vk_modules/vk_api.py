from modules.fetch_photos_info.fetch_photos_info import fetch_photo_data
from modules.vk_modules.vk_photo_processor import VKPhotoProcessor

API_VERSION: float | int = 5.199
URL: str = 'https://api.vk.com/method/'
DATE_FORMAT: str = '%Y-%m-%d'
PREFERRED_SIZES: str | list = ['w', 'z']


class VkProfilePhotosRetriever(VKPhotoProcessor):
	def __init__(
			self, token: str, method: str, user_id: int,
			album_id: str = 'wall', count: int = 5
	) -> None:
		self.method: str = method
		self.params: dict = {
			'access_token': token,
			'owner_id': user_id,
			'album_id': album_id,
			'count': count,
			'extended': 1,
			'photo_sizes': 1,
			'v': API_VERSION,
		}

	def get_photos_info(self):
		data = fetch_photo_data(URL, self.method, self.params)

		if 'response' in data and 'items' in data['response']:
			photos = data['response']['items']
			extracted_photo_info = self._extract_photo_info(
				photos, DATE_FORMAT, PREFERRED_SIZES
			)
			return extracted_photo_info
		else:
			raise ValueError('Не удалось получить данные о фотографиях')
