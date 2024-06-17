import requests


class GetVkPhotos:
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
		photos_info = self.get_photos_info()['response']['items']
		photos_list = []
		for photo in photos_info:
			test = ''
			for size in photo['sizes']:
				if size['type'] == 'w':
					test = size['url']
				elif size['type'] == 'z':
					test = size['url']

			photos_list.append({
				'likes': photo['likes']['count'],
				'date': photo['date'],
				'sizes': test
			})

		return photos_list


test = GetVkPhotos('service_info/vk_token.txt', 133468233, 'profile', 2).get_photos()
