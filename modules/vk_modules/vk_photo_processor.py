import time
from typing import List, Any
from modules.unix_to_date.unix_to_date import UnixToDate
from tqdm import tqdm


class VKPhotoProcessor:
	"""A class to process and extract information from VK photos."""

	def _extract_photo_info(self, photos, date_format: str, preferred_size: str = 'z') -> dict[
		str, list]:
		"""
		Extracts information from a list of photo objects.

		Args:
			photos: A list of photo objects retrieved from the VK API.
			date_format: The format to use for converting Unix timestamps to dates.
			preferred_size: The preferred photo size to extract (default: 'z').

		Returns:
			A dictionary containing two lists: 'full_info' and 'json'. 'full_info' contains
		detailed information about each photo, while 'json' contains a simplified version of the
		data.
		"""
		extracted_photo_info = {'full_info': [], 'json': []}
		for photo in tqdm(photos, desc="Получение и обработка данных о фотографии", unit="фото"):
			time.sleep(0.5)
			sizes = photo.get('sizes', [])
			likes_count = photo.get('likes', {}).get('count', 0)
			date = UnixToDate(photo['date'], date_format).convert()
			filename = self._create_filename(photo, photo['likes']['count'], date,
											 extracted_photo_info['full_info'])
			size_url, size_type = self._find_preferred_size_url(sizes, preferred_size)
			extracted_photo_info['full_info'].append({
				'filename': f'{filename}.jpg',
				'url': size_url,
				'likes': likes_count,
				'date': date
			})
			extracted_photo_info['json'].append({'filename': f'{filename}.jpg', 'size': size_type})
		return extracted_photo_info

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
		duplicates = [item for item in photo_list if item["likes"] == likes and item != photo]
		return f"{likes}" + (f"_{date}" if duplicates else "")
