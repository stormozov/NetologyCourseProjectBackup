import os
import json
import pprint
import requests


class GetVkToken:
	def __init__(self, token, user_id, album_id, count=5):
		self.url = 'https://api.vk.com/method/photos.get'
		self.params = {
			'access_token': token,
			'owner_id': user_id,
			'album_id': album_id,
			'count': count,
			'extended': 1,
			'photo_sizes': 1,
			'v': 5.131,
		}


class GetVkPhotos(GetVkToken):
	def get_photos_info(self):
		return requests.get(self.url, params=self.params).json()


with open('service_info/vk_token.txt', encoding='utf-8') as f:
	token = f.read().strip()
	photos = GetVkPhotos(token, 133468233, 'profile', 12).get_photos_info()
	pprint.pprint(photos['response']['items'])
