import requests
from modules.vk_modules.vk_photo_processor import VKPhotoProcessor

import pprint


class VkProfilePhotosRetriever(VKPhotoProcessor):
	API_VERSION: int = 5.199
	URL: str = 'https://api.vk.com/method/photos.get'
	DATE_FORMAT: str = '%Y-%m-%d %H-%M-%S'
	PREFERRED_SIZES = {'w', 'z'}

	def __init__(self, token_path: str, user_id: int, album_id: str = 'wall', count: int = 5):
		self.token_path = token_path
		self.params = {
			'access_token': '',
			'owner_id': user_id,
			'album_id': album_id,
			'count': count,
			'extended': 1,
			'photo_sizes': 1,
			'v': self.API_VERSION,
		}

	def retrieve_photo_data(self):
		with open(self.token_path, encoding='utf-8') as f:
			self.params['access_token'] = f.read().strip()
			try:
				response = requests.get(self.URL, params=self.params)
				response.raise_for_status()
				return response.json()
			except requests.exceptions.RequestException as e:
				print(f"Error during HTTP request: {e}")
				return None

	def get_photos(self):
		response = self.retrieve_photo_data()
		if 'response' in response and 'items' in response['response']:
			photos = response['response']['items']
			photo_list = self._extract_photo_info(photos, self.DATE_FORMAT, self.PREFERRED_SIZES)
			return photo_list
		else:
			return []


test = VkProfilePhotosRetriever('service_info/vk_token.txt', 133468233, 'profile', 2).get_photos()
pprint.pprint(test)