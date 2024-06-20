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
    with open(filename, "w") as file:
        json.dump(data, file)
