from modules.unix_to_date.unix_to_date import UnixToDate


class VKPhotoProcessor:
	def _extract_photo_info(self, photos, date_format: str, preferred_size='z') -> dict[str, list]:
		extracted_photo_info = {'full_info': [], 'json': []}
		for photo in photos:
			sizes = photo.get('sizes', [])
			likes_count = photo['likes'].get('count', 0) if 'likes' in photo else 0
			date = UnixToDate(photo['date'], date_format).convert()
			filename = self._create_filename(photo, photo['likes']['count'], date, extracted_photo_info['full_info'])
			size_url, size_type = self._find_preferred_size_url(sizes, preferred_size)
			extracted_photo_info['full_info'].append({
				'filename': f'{filename}.jpg',
				'url': size_url,
				'likes': likes_count,
				'date': date
			})
			extracted_photo_info['json'].append({'filename': f'{filename}.jpg', 'size': size_type})
		return extracted_photo_info

	def _find_preferred_size_url(self, sizes: list, preferred_size: str = 'z'):
		return next(([size['url'], size['type']] for size in sizes if size['type'] in preferred_size), None)

	def _create_filename(self, photo, likes, date, photo_list) -> str:
		duplicates = [item for item in photo_list if item["likes"] == likes and item != photo]
		filename = f"{likes}" + (f"_{date}" if duplicates else "")
		return filename
