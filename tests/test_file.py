import hashlib
import json
import os
from pathlib import Path

import pytest
from pytest_mock import MockerFixture


class TestFileUtil:

    @pytest.fixture
    def path_exists_mock(self, module_patch):
        return module_patch("os.path.exists")

    @pytest.fixture
    def mock_path_separator(self, module_patch):
        return lambda separator: module_patch("os.path.sep", new=separator)

    @pytest.fixture
    def listdir_mock(self, module_patch):
        return module_patch("os.listdir")

    @pytest.fixture
    def remove_mock(self, module_patch):
        return module_patch("os.remove")

    def test_should_not_cleanup_non_existing_dir(self, listdir_mock):

        from kutil.file import cleanup_directory

        cleanup_directory("non/existing/dir")
        listdir_mock.assert_not_called()

    def test_should_remove_all_contents(self, tmp_path: Path):

        from kutil.file import cleanup_directory, save_file

        test_dir = tmp_path / "TestDir"
        nested_test_dir = test_dir / "AnotherTestDir"

        os.mkdir(test_dir)
        os.mkdir(nested_test_dir)

        save_file(str(test_dir / "test.json"), {}, as_json=True)
        save_file(str(nested_test_dir / "test.txt"), "")

        cleanup_directory(str(test_dir))

        assert len(os.listdir(str(test_dir))) == 0
        assert not os.path.exists(str(nested_test_dir))

    def test_should_handle_error_silently_when_cleanup_dir(self, mocker: MockerFixture, tmp_path: Path, module_patch):

        from kutil.file import cleanup_directory, save_file

        print_mock = mocker.patch("builtins.print")
        unlink_mock = module_patch("os.unlink")
        unlink_mock.side_effect = RuntimeError("Can't unlink")

        test_dir = tmp_path / "TestDir"
        os.mkdir(test_dir)

        save_file(str(test_dir / "test.json"), {}, as_json=True)
        cleanup_directory(str(test_dir))

        print_mock.assert_called_once()

    def test_should_fail_read_file_if_doesnt_exist(self):

        from kutil.file import read_file

        with pytest.raises(RuntimeError):
            read_file("non_existing.txt")

    def test_read_file_basic_text(self, tmp_path):

        from kutil.file import read_file

        content = "Hello, this is a test line.\nAnother line."
        file_path = tmp_path / "test_file.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        actual_content = read_file(str(file_path), as_json=False)

        assert actual_content == content

    def test_read_file_as_json(self, tmp_path):

        from kutil.file import read_file

        json_data = {"name": "Test User", "id": 123, "active": True}
        json_content = json.dumps(json_data)

        file_path = tmp_path / "test_data.json"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json_content)

        actual_data = read_file(str(file_path), as_json=True)

        assert actual_data == json_data
        assert isinstance(actual_data, dict)

    def test_read_file_invalid_json(self, tmp_path):

        from kutil.file import read_file

        invalid_content = "{'key': 'value'"
        file_path = tmp_path / "bad_data.json"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(invalid_content)

        with pytest.raises(json.JSONDecodeError):
            read_file(str(file_path), as_json=True)

    def test_save_file_plain_text(self, tmp_path):

        from kutil.file import save_file

        content = "A simple line of text.\nWith a second line."
        file_path = tmp_path / "text_output.txt"

        save_file(str(file_path), content)

        with open(file_path, "r", encoding="utf-8") as f:
            actual_content = f.read()

        assert actual_content == content

    def test_save_file_binary_data(self, tmp_path):

        from kutil.file import save_file

        binary_data = b'\xde\xad\xbe\xef\x00\x01\x02'
        file_path = tmp_path / "binary_output.bin"

        save_file(str(file_path), binary_data, binary=True)

        with open(file_path, "rb") as f:
            actual_data = f.read()

        assert actual_data == binary_data

    def test_save_file_as_json_text_mode(self, tmp_path):

        from kutil.file import save_file

        data = {"key1": "value1", "key2": [1, 2, 3]}
        file_path = tmp_path / "json_output.json"
        expected_content = '{\n  "key1": "value1",\n  "key2": [\n    1,\n    2,\n    3\n  ]\n}'

        save_file(str(file_path), data, as_json=True)

        with open(file_path, "r", encoding="utf-8") as f:
            actual_content = f.read()

        actual_data = json.loads(actual_content)
        assert actual_content.strip() == expected_content.strip()
        assert actual_data == data

    def test_should_delete_file(self, module_patch, tmp_path, path_exists_mock, remove_mock):

        from kutil.file import delete_file

        path_exists_mock.return_value = False

        delete_file(str(tmp_path / "non_existing.txt"))
        remove_mock.assert_not_called()

        path_exists_mock.return_value = True
        delete_file(str(tmp_path / "test.txt"))
        remove_mock.assert_called_once()

    def test_file_checksum_basic_sha256(self, tmp_path):

        from kutil.file import file_checksum

        content = b"test"
        file_path = tmp_path / "test_file.txt"

        with open(file_path, "wb") as f:
            f.write(content)

        expected_hash = hashlib.sha256(content).hexdigest()
        actual_hash = file_checksum(str(file_path), algorithm="sha256")

        assert actual_hash == expected_hash

    def test_file_name_from_path(self, mock_path_separator):

        from kutil.file import file_name_from_path

        mock_path_separator("/")

        assert file_name_from_path("long/path/to/test.txt") == "test.txt"

        mock_path_separator("\\")
        assert file_name_from_path("D:\\long\\path\\to\\test.txt") == "test.txt"
        assert file_name_from_path("test.txt") == "test.txt"
        assert file_name_from_path("test") == "test"

    def test_remove_extension_from_path(self):

        from kutil.file import remove_extension_from_path

        assert remove_extension_from_path("test") == "test"
        assert remove_extension_from_path("test.txt") == "test"
        assert remove_extension_from_path("D:\\path\\to\\file.txt") == "D:\\path\\to\\file"
        assert remove_extension_from_path("/root/test/file.txt") == "/root/test/file"
