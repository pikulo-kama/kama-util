

class TestFileExtension:

    def test_file_extension(self):

        from kutil.file_type import FileType

        cfg_extension: FileType = FileType("cfg")

        assert cfg_extension.__str__() == ".cfg"
        assert cfg_extension.extension == ".cfg"
        assert cfg_extension.no_dot == "cfg"
        assert cfg_extension.remove_extension("test") == "test"
        assert cfg_extension.remove_extension("test.cfg") == "test"
        assert cfg_extension.add_extension("test.cfg") == "test.cfg"
        assert cfg_extension.add_extension("test") == "test.cfg"
