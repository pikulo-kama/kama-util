import hashlib
import json
import os.path
import shutil
from typing import Any


def cleanup_directory(directory: str):
    """
    Used to delete all contents of directory.
    """

    if not os.path.exists(directory):
        return

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)

            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def read_file(file_path: str, as_json: bool = False):
    """
    Used to read contents of the file.
    Throws exception if file doesn't exist.
    """

    if not os.path.exists(file_path):
        raise RuntimeError(f"File {file_path} doesn't exist.")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file) if as_json else file.read()


def save_file(file_path: str, data: Any, as_json: bool = False, binary: bool = False):
    """
    Used to save contents of the file.
    """

    mode = "wb" if binary else "w"
    encoding = None if binary else "utf-8"

    with open(file_path, mode, encoding=encoding) as file:

        if as_json:
            json.dump(data, file, indent=2, ensure_ascii=False)  # noqa
        else:
            file.write(data)


def delete_file(file_path: str):
    """
    Used to remove file.
    """

    if os.path.exists(file_path):
        os.remove(file_path)


def file_checksum(file_path: str, algorithm: str = "sha256", block_size: int = 8192):
    """
    Used to get checksum of file.
    """

    file_hash = hashlib.new(algorithm)

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(block_size), b""):
            file_hash.update(chunk)

    return file_hash.hexdigest()


def file_name_from_path(file_path: str):
    """
    Used to extract file name from file path.
    e.g. /path/to/file.txt -> file.txt
    """

    if os.path.sep not in file_path:
        return file_path

    return file_path[file_path.rindex(os.path.sep) + 1:]


def remove_extension_from_path(file_path: str):
    """
    Used to remove file extension from file path.
    e.g. /path/to/file.txt -> /path/to/file
    """

    separator = "."

    if separator not in file_path:
        return file_path

    return file_path[0:file_path.rindex(separator)]
