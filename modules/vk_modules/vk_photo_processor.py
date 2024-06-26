import time
from typing import Union
from tqdm import tqdm
from modules.vk_modules.utils import *


class VKPhotoProcessor:
	"""A class to process and extract information from VK photos."""

	def __init__(self, photos: list[dict], date_format: str, preferred_size: str) -> None:
		"""
		Initializes the VKPhotoProcessor instance.

		Args:
			photos (list[dict]): The list of photos to extract data from.
			date_format (str): The format for converting Unix timestamps to dates.
			preferred_size (str): The preferred size type to search for.
		"""
		self.photos = photos
		self.date_format = date_format
		self.preferred_size = preferred_size

	def get_photo_info(self) \
		-> dict[str, Union[int, str, list]]:
		"""
		Extracts relevant data from a list of photos.

		Returns:
			dict[str, Union[int, str, list]]: A dictionary containing extracted photo information.
				- 'full_info' (list): A list of dictionaries with detailed photo information.
				- 'json' (list): A list of dictionaries with photo filenames and size types.
		"""
		extracted_photo_info: dict[str, Union[int, str, list]] = {'full_info': [], 'json': []}

		for photo in tqdm(
			self.photos, desc="Получение и обработка данных о фотографии", unit="фото"
		):
			time.sleep(0.5)
			photo_data = extract_photo_data(photo, self.date_format)
			size_url, size_type = find_preferred_size_url(photo_data['sizes'], self.preferred_size)
			filename = create_filename(
				photo, photo_data['likes'], photo_data['date'],
				extracted_photo_info['full_info']
			)
			append_full_info(extracted_photo_info, filename, size_url, photo_data)
			append_json(extracted_photo_info, filename, size_type)

		return extracted_photo_info
