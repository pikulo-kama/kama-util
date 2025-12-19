

class FileExtension:
    """
    Represents a file extension and provides utility methods for path manipulation.

    This class helps in consistently adding or removing extensions from strings 
    and provides formats with or without the leading dot.
    """

    def __init__(self, extension: str):
        """
        Initializes the FileExtension with the raw extension string.
        """
        self.__extension = extension

    @property
    def with_dot(self):
        """
        Returns the extension with a leading dot (e.g., '.json').
        """
        return f".{self.no_dot}"

    @property
    def no_dot(self):
        """
        Returns the raw extension without a leading dot (e.g., 'json').
        """
        return self.__extension

    def add_to(self, string: str):
        """
        Appends the extension to a string if it is not already present.

        Checks if the string ends with the dot-prefixed extension before 
        concatenating to avoid duplication.
        """

        if string.endswith(self.with_dot):
            return string

        return string + self.with_dot

    def remove_from(self, string: str):
        """
        Removes all occurrences of the dot-prefixed extension from the string.
        """
        return string.replace(self.with_dot, "")

    def __str__(self):
        """
        Returns the string representation of the extension (with dot).
        """
        return self.with_dot


JSON = FileExtension("json")
LOG = FileExtension("log")
