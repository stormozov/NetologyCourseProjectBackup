import requests
import datetime


class GetVkProfilePhotos:
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

	def get_photos_info(self):
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
		response = self.get_photos_info()
		if 'response' in response and 'items' in response['response']:
			photos = response['response']['items']
			photo_list = self._process_photos(photos)
			return photo_list
		else:
			return []

	def _unix_to_date(self, unix_time: int) -> str:
		try:
			return datetime.datetime.fromtimestamp(unix_time).strftime(self.DATE_FORMAT)
		except Exception as e:
			print(f"Error converting unix time to date: {e}")
			return ''

	def _process_photos(self, photos):
		photo_list = []
		for photo in photos:
			sizes = photo.get('sizes', [])
			likes_count = photo['likes'].get('count', 0) if 'likes' in photo else 0
			size_url = self._get_size_url(sizes) or 'default_url'
			photo_list.append({
				'likes': likes_count,
				'date': self._unix_to_date(photo['date']),
				'url': size_url
			})
		return photo_list

	def _get_size_url(self, sizes: list):
		# Return the url for the preferred size types
		return next((size['url'] for size in sizes if size['type'] in self.PREFERRED_SIZES), None)


test = GetVkProfilePhotos('service_info/vk_token.txt', 133468233, 'profile', 2).get_photos()
