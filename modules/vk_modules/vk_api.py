from modules.fetch_photos_info.fetch_photos_info import fetch_photo_data
from modules.vk_modules.vk_photo_processor import VKPhotoProcessor

API_VERSION: float | int = 5.199
URL: str = 'https://api.vk.com/method'
DATE_FORMAT: str = '%Y-%m-%d'
PREFERRED_SIZES: str | list = ['w', 'z']


class VkProfilePhotosRetriever:
	"""Retrieves photos from a VK profile."""

	def __init__(
			self, token: str, method: str, user_id: int,
			album_id: str = 'wall', count: int = 5
	) -> None:
		"""
		Initializes the VkProfilePhotosRetriever instance.

		Args:
			token: The access token for the VK API.
			method: The VK API method to use for retrieving photos.
			user_id: The ID of the VK user whose photos to retrieve.
			album_id: The ID of the album to retrieve photos from (default: 'wall').
			count: The number of photos to retrieve (default: 5).
		"""
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

	def get_photos_info(self) -> dict[str, list]:
		"""
		Retrieves photos from the VK API and extracts their information.

		Returns:
			A dictionary with two keys:
			- 'full_info': a list of dictionaries containing photo information.
			- 'json': the original JSON response from the VK API.

		Raises:
			ValueError: If the VK API returns an error or no photos are found.
		"""
		data: dict = fetch_photo_data(URL, self.method, self.params)

		if 'response' in data and 'items' in data['response']:
			photos = data['response']['items']
			extracted_photo_info: dict[str, list] = VKPhotoProcessor(
				photos, DATE_FORMAT, PREFERRED_SIZES
			).get_photo_info()
			return extracted_photo_info
		else:
			raise ValueError('Не удалось получить данные о фотографиях')
