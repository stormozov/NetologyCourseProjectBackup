import json


def create_json_file(data: list[dict], filename: str = "result.json") -> None:
    """
    This function creates a JSON file named "result.json"
    and writes the JSON-serialized data_info into it.

    Args:
        - data (Any): The data to be serialized into JSON format.
        - filename (str, optional): The name of the JSON file. Defaults to "result.json".

    Returns:
        None
    """
    if not data:
        return
    if not isinstance(data, list):
        raise TypeError("data must be a list")
    if not all(isinstance(item, dict) for item in data):
        raise TypeError("all items in data must be dicts")
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")

    try:
        with open(filename, "w") as file:
            json.dump(data, file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} not found")
    except PermissionError:
        raise PermissionError(f"Permission denied when trying to write to {filename}")
