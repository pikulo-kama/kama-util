

class FileType:
    """
    Represents a file extension and provides utility methods for path manipulation.

    This class helps in consistently adding or removing extensions from strings 
    and provides formats with or without the leading dot.
    """

    def __init__(self, stem: str, mime_type: str):
        """
        Initializes the FileExtension with the raw extension string.
        """

        self.__stem = stem
        self.__mime_type = mime_type

    @property
    def extension(self):
        """
        Returns the extension with a leading dot (e.g., '.json').
        """
        return f".{self.stem}"

    @property
    def stem(self):
        """
        Returns the raw extension without a leading dot (e.g., 'json').
        """
        return self.__stem

    @property
    def mime_type(self):
        return self.__mime_type

    def add_extension(self, string: str):
        """
        Appends the extension to a string if it is not already present.

        Checks if the string ends with the dot-prefixed extension before 
        concatenating to avoid duplication.
        """

        if string.endswith(self.extension):
            return string

        return string + self.extension

    def remove_extension(self, string: str):
        """
        Removes all occurrences of the dot-prefixed extension from the string.
        """
        return string.replace(self.extension, "")

    def __str__(self):
        """
        Returns the string representation of the extension (with dot).
        """
        return self.extension


JSON = FileType("json", "application/json")
LOG = FileType("log", "text/plain")
YML = FileType("yml", "application/x-yaml")
YAML = FileType("yaml", "application/x-yaml")
JPG = FileType("jpg", "image/jpeg")
SVG = FileType("svg", "image/svg+xml")
ZIP = FileType("zip", "application/zip")
