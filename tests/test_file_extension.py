

class TestFileExtension:

    def test_file_extension(self):

        from kutil.file_extension import FileExtension

        cfg_extension: FileExtension = FileExtension("cfg")

        assert cfg_extension.__str__() == ".cfg"
        assert cfg_extension.with_dot == ".cfg"
        assert cfg_extension.no_dot == "cfg"
        assert cfg_extension.remove_from("test") == "test"
        assert cfg_extension.remove_from("test.cfg") == "test"
        assert cfg_extension.add_to("test.cfg") == "test.cfg"
        assert cfg_extension.add_to("test") == "test.cfg"
