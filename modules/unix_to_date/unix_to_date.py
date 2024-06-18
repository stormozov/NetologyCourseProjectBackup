import datetime


class UnixToDate:
	"""
	A class to convert Unix timestamp to a formatted date string.

	Attributes:
		unix_time (int): The Unix timestamp to be converted to date.
		date_format (str): The format in which the date should be returned.

	Methods:
		convert(): Converts the Unix timestamp to a formatted date string based on the
	provided date format. Returns the formatted date string or an empty string if an error occurs
	during conversion.
	"""

	def __init__(self, unix_time: int, date_format: str):
		self.unix_time = unix_time
		self.date_format = date_format

	def convert(self):
		try:
			return datetime.datetime.fromtimestamp(self.unix_time).strftime(self.date_format)
		except Exception as e:
			print(f"Error converting unix time to date: {e}")
			return ''
