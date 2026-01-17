

class TestFileExtension:

    def test_file_extension(self):

        from kutil.file_type import FileType

        cfg_extension: FileType = FileType("cfg", "application/cfg")

        assert cfg_extension.__str__() == ".cfg"
        assert cfg_extension.extension == ".cfg"
        assert cfg_extension.stem == "cfg"
        assert cfg_extension.mime_type == "application/cfg"
        assert cfg_extension.remove_extension("test") == "test"
        assert cfg_extension.remove_extension("test.cfg") == "test"
        assert cfg_extension.add_extension("test.cfg") == "test.cfg"
        assert cfg_extension.add_extension("test") == "test.cfg"
