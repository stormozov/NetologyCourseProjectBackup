import time
from typing import Union
from modules.unix_to_date.unix_to_date import UnixToDate
from tqdm import tqdm


class VKPhotoProcessor:
	"""A class to process and extract information from VK photos."""

	def get_photo_info(self, photos, date_format: str, preferred_size: str) \
		-> dict[str, Union[int, str, list]]:
		"""
		Extracts relevant data from a list of photos.

		Args:
			photos: The list of photos to extract data from.
			date_format: The format for converting Unix timestamps to dates.
			preferred_size: The preferred size type to search for.

		Returns:
			dict[str, Union[int, str, list]]: A dictionary containing extracted photo information.
				- 'full_info' (list): A list of dictionaries with detailed photo information.
				- 'json' (list): A list of dictionaries with photo filenames and size types.
		"""
		extracted_photo_info: dict[str, Union[int, str, list]] = {'full_info': [], 'json': []}

		for photo in tqdm(photos, desc="Получение и обработка данных о фотографии", unit="фото"):
			time.sleep(0.5)
			photo_data: dict[str, any] = self._extract_photo_data(photo, date_format)
			size_url, size_type = self._find_preferred_size_url(photo_data['sizes'], preferred_size)
			filename: str = self._create_filename(
				photo, photo_data['likes'], photo_data['date'],
				extracted_photo_info['full_info']
			)
			extracted_photo_info['full_info'].append({
				'filename': f'{filename}.jpg',
				'url': size_url,
				'likes': photo_data['likes'],
				'date': photo_data['date']
			})
			extracted_photo_info['json'].append({'filename': f'{filename}.jpg', 'size': size_type})

		return extracted_photo_info

	@staticmethod
	def _extract_photo_data(photo: dict, date_format: str) -> dict[str, any]:
		"""
		Extracts relevant data from a photo dictionary.

		Args:
			photo (dict): A dictionary containing photo data.
			date_format (str): The format to use for converting Unix timestamps to dates.

		Returns:
			dict: A dictionary containing the following keys:
				- 'likes' (int): The number of likes for the photo.
				- 'date' (str): The date the photo was taken.
				- 'sizes' (list): A list of dictionaries representing different sizes of the image.
		"""
		likes_count: int = photo.get('likes', {}).get('count', 0)
		date: str = UnixToDate(photo['date'], date_format).convert()
		sizes: list = photo.get('sizes', [])
		return {'likes': likes_count, 'date': date, 'sizes': sizes}

	@staticmethod
	def _find_preferred_size_url(sizes: list, preferred_size: str = 'z') -> tuple[str, str]:
		"""
		Finds the URL and type of the preferred size of an image from a list of image sizes.

		Args:
			sizes (list): A list of dictionaries representing different sizes of the image.
			preferred_size (str): The preferred size type to search for (default is 'z').

		Returns:
			Tuple[str, str]: A tuple containing the URL and type of the preferred size image.

		Raises:
			ValueError: If the preferred size type is not found in any of the image sizes.
		"""
		try:
			for size in sizes:
				if size['type'] in preferred_size:
					return size['url'], size['type']
		except KeyError:
			raise ValueError('Не удалось найти предпочтительный размер изображения')

	@staticmethod
	def _create_filename(photo, likes, date, photo_list) -> str:
		"""
		Creates a unique filename for a photo based on its likes and date.

		The default filename will include the number of likes for a photo. If there are several
		photos with the same number of likes, the date when the photo was published will be added
		after the number of likes in the filename.

		Args:
			photo: The photo object.
			likes: The number of likes for the photo.
			date: The date of the photo.
			photo_list: A list of photo objects to check for duplicates.

		Returns:
			A unique filename for the photo.
		"""
		duplicates = [item for item in photo_list if item['likes'] == likes and item != photo]
		return f'{likes}' + (f'_{date}' if duplicates else '')
