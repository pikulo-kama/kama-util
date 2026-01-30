
import requests
from kutil.file import save_file


def url_retrieve(url: str, path: str) -> bool:
    """
    Downloads a file from a URL to a local path.

    :param url: The direct link to the file to be downloaded.
    :param path: The local file path (including filename) where the file will be saved.
    :return: True if the download was successful, False if a network or disk error occurred.
    """

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an error for 4xx or 5xx responses

        save_file(path, response.content, binary=True)
        return True

    except requests.RequestException:
        return False
