from modules.unix_to_date.unix_to_date import UnixToDate


class VKPhotoProcessor:
	def _extract_photo_info(self, photos, date_format: str, preferred_size='z'):
		photo_list = []
		for photo in photos:
			sizes = photo.get('sizes', [])
			likes_count = photo['likes'].get('count', 0) if 'likes' in photo else 0
			date = UnixToDate(photo['date'], date_format).convert()
			size_url, size_type = self._find_preferred_size_url(sizes, preferred_size)
			photo_list.append({
				'likes': likes_count,
				'date': date,
				'size_type': size_type,
				'url': size_url
			})
		return photo_list

	def _find_preferred_size_url(self, sizes: list, preferred_size: str = 'z'):
		return next(([size['url'], size['type']] for size in sizes if size['type'] in preferred_size), None)