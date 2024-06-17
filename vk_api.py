import requests


class GetVkProfilePhotos:
	def __init__(self, token_path, user_id, album_id='wall', count=5):
		self.url = 'https://api.vk.com/method/photos.get'
		self.token_path = token_path
		self.params = {
			'access_token': '',
			'owner_id': user_id,
			'album_id': album_id,
			'count': count,
			'extended': 1,
			'photo_sizes': 1,
			'v': 5.199,
		}

	def get_photos_info(self):
		with open(self.token_path, encoding='utf-8') as f:
			self.params['access_token'] = f.read().strip()
			return requests.get(self.url, params=self.params).json()

	def get_photos(self):
		response = self.get_photos_info()
		photos = response['response']['items']
		photo_list = self._process_photos(photos)
		return photo_list

	def _process_photos(self, photos):
		photo_list = []
		for photo in photos:
			sizes = photo['sizes']
			size_url = self._get_size_url(sizes)
			photo_list.append({
				'likes': photo['likes']['count'],
				'date': photo['date'],
				'url': size_url
			})
		return photo_list

	def _get_size_url(self, sizes):
		for size in sizes:
			if size['type'] in ['w', 'z']:
				return size['url']
		return None


test = GetVkProfilePhotos('service_info/vk_token.txt', 133468233, 'profile', 2).get_photos()
