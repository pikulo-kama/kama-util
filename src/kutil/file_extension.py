

class FileExtension:

    def __init__(self, extension: str):
        self.__extension = extension

    @property
    def with_dot(self):
        return f".{self.no_dot}"

    @property
    def no_dot(self):
        return self.__extension

    def add_to(self, string: str):

        if string.endswith(self.with_dot):
            return string

        return string + self.with_dot

    def remove_from(self, string: str):
        return string.replace(self.with_dot, "")

    def __str__(self):
        return self.with_dot

JSON = FileExtension("json")
LOG = FileExtension("log")
