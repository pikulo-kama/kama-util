import pytest


@pytest.fixture
def module_patch(get_module_patch):
    return get_module_patch("kutil")

@pytest.fixture
def path_join_mock(module_patch):
    return module_patch("os.path.join", side_effect=lambda *args: "/".join(args))
