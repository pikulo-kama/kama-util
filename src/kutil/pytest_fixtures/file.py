import pytest


@pytest.fixture
def cleanup_directory_mock(module_patch):
    return module_patch("cleanup_directory")

@pytest.fixture
def read_file_mock(module_patch):
    return module_patch("read_file")

@pytest.fixture
def save_file_mock(module_patch):
    return module_patch("save_file")

@pytest.fixture
def delete_file_mock(module_patch):
    return module_patch("delete_file")

@pytest.fixture
def file_checksum_mock(module_patch):
    return module_patch("file_checksum")

@pytest.fixture
def file_name_from_path_mock(module_patch):
    return module_patch("file_name_from_path")

@pytest.fixture
def remove_extension_from_path_mock(module_patch):
    return module_patch("remove_extension_from_path")
