import hashlib
import json
import os.path
import shutil
import sys
from pathlib import Path
from typing import Any


def cleanup_directory(directory: str):
    """
    Used to delete all contents of directory.

    Iterates through the specified directory and removes every file,
    symbolic link, or subdirectory encountered. If the target directory
    itself does not exist, the function returns immediately.
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

    Reads the raw text of a file or parses it as a JSON object if the
    flag is set. Uses UTF-8 encoding by default.
    """

    if not os.path.exists(file_path):
        raise RuntimeError(f"File {file_path} doesn't exist.")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file) if as_json else file.read()


def save_file(file_path: str, data: Any, as_json: bool = False, binary: bool = False):
    """
    Used to save contents of the file.

    Writes data to a file. Supports standard text writing, binary
    mode for non-text data, and JSON serialization with non-ASCII
    characters preserved.
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

    Silently checks if the file exists before attempting to delete it
    to prevent errors.
    """

    if os.path.exists(file_path):
        os.remove(file_path)


def file_checksum(file_path: str, algorithm: str = "sha256", block_size: int = 8192):
    """
    Used to get checksum of file.

    Calculates a cryptographic hash of the file's contents. Reads the
    file in chunks to ensure low memory usage even with large files.
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

    Identifies the last component of a path using the operating
    system's specific path separator.
    """

    if os.path.sep not in file_path:
        return file_path

    return file_path[file_path.rindex(os.path.sep) + 1:]


def remove_extension_from_path(file_path: str):
    """
    Used to remove file extension from file path.
    e.g. /path/to/file.txt -> /path/to/file

    Truncates the string starting from the last occurrence of the
    dot separator.
    """

    separator = "."

    if separator not in file_path:
        return file_path

    return file_path[0:file_path.rindex(separator)]


def get_runtime_root() -> Path:
    """
    Returns the root directory of the application.
    Works for:
    1. Standard Python scripts (searching for markers).
    2. Compiled .exe files (PyInstaller/Nuitka).
    """

    # 1. Check if the app is running as a compiled bundle (.exe)
    if getattr(sys, "frozen", False):
        # If frozen, sys.executable is the path to the actual .exe file
        return Path(sys.executable).parent

    # 2. If running as a normal script, use the marker-based search
    # Starting from the script entry point
    start_path = Path(sys.argv[0]).resolve()
    if not start_path.exists():
        start_path = Path.cwd().resolve()

    root_markers = {".git", "pyproject.toml", "requirements.txt", ".root"}

    for parent in [start_path] + list(start_path.parents):
        if any((parent / marker).exists() for marker in root_markers):
            return parent

    # Fallback to current working directory
    return Path.cwd().resolve()
