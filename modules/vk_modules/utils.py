from modules.unix_to_date.unix_to_date import UnixToDate


def append_full_info(photo_list: dict[str, list], filename: str, size_url: str, photo_data: dict) -> None:
	"""
	Appends detailed information about a photo to the 'full_info' list in the photo_list.

	Args:
		photo_list (dict): The dictionary containing the photo information lists.
		filename (str): The filename of the photo.
		size_url (str): The URL of the photo's size.
		photo_data (dict): The dictionary containing photo data including likes and date.
	"""
	photo_list['full_info'].append({
		'filename': f'{filename}.jpg',
		'url': size_url,
		'likes': photo_data['likes'],
		'date': photo_data['date']
	})


def append_json(photo_list: dict[str, list], filename: str, size_type: str) -> None:
	"""
	Appends the filename and size type to the 'json' list in the photo_list.

	Args:
		photo_list (dict): The dictionary containing the photo information lists.
		filename (str): The filename of the photo.
		size_type (str): The size type of the photo.
	"""
	photo_list['json'].append({'filename': f'{filename}.jpg', 'size': size_type})


def extract_photo_data(photo: dict, date_format: str) -> dict[str, any]:
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


def find_preferred_size_url(sizes: list, preferred_size: str = 'z') -> tuple[str, str]:
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


def create_filename(photo, likes, date, photo_list) -> str:
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
	duplicates: list = [item for item in photo_list if item['likes'] == likes and item != photo]
	return f'{likes}' + (f'_{date}' if duplicates else '')