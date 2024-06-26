from typing import Union, Dict
import requests


def fetch_photo_data(url: str, method: str, params: Dict[str, Union[str, int]]) \
	-> Union[Dict[str, str], None]:
	"""
	Fetches photo data from the specified URL using the provided method and parameters.

	Parameters:
		- url (str): The base URL to send the request to.
		- method (str): The HTTP method to use for the request.
		- params (Dict[str, str]): The parameters to include in the request.

	Returns:
		- Union[Dict[str, str], None]: The JSON response data if the request is successful, None otherwise.

	Raises:
		- requests.exceptions.RequestException: If an error occurs during the HTTP request.

	Example:
		>>> fetch_photo_data('https://example.com', 'photos', {'user_id': '123', 'album_id': '456'})
		{
			'photo1': {'url': 'https://example.com/photos/1.jpg', 'likes': 10},
			'photo2': {'url': 'https://example.com/photos/2.jpg', 'likes': 5}
		}
	"""
	try:
		response = requests.get(f'{url}/{method}', params=params)
		if response.status_code == 200:
			return response.json()
		else:
			raise requests.RequestException(f'Error: Invalid response code — {response.status_code}')
	except requests.exceptions.RequestException as e:
		raise requests.RequestException(f"Error during HTTP request: {e}")
