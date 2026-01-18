import pytest


@pytest.fixture
def path_join_mock(module_patch):
    return module_patch("os.path.join", side_effect=lambda *args: "/".join(args))

@pytest.fixture
def path_exists_mock(module_patch):
    return module_patch("os.path.exists")
