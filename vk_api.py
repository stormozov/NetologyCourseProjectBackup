import os
import json
import pprint
import requests


class GetVkPhotos:
	def __init__(self, token, user_id, album_id, count=5):
		self.url = 'https://api.vk.com/method/photos.get'
		self.token_path = token
		self.params = {
			'access_token': token,
			'owner_id': user_id,
			'album_id': album_id,
			'count': count,
			'extended': 1,
			'photo_sizes': 1,
			'v': 5.131,
		}

	def get_photos_info(self):
		with open(self.token_path, encoding='utf-8') as f:
			self.params['access_token'] = f.read().strip()
			return requests.get(self.url, params=self.params).json()


test = GetVkPhotos('service_info/vk_token.txt', 133468233, 'profile', 12).get_photos_info()
pprint.pprint(test)
