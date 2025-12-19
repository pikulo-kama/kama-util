import pytest
from _pytest.fixtures import FixtureRequest
from pytest_mock import MockerFixture


@pytest.fixture
def safe_patch(mocker: MockerFixture):
    from kutil.pytest import safe_patch_fixture
    return safe_patch_fixture(mocker)

@pytest.fixture
def safe_module_patch(get_module_patch):
    from kutil.pytest import safe_module_patch_fixture
    return safe_module_patch_fixture(get_module_patch)

@pytest.fixture
def module_path(request: FixtureRequest):
    from kutil.pytest import module_path_fixture
    return module_path_fixture(request)

@pytest.fixture
def get_module_patch(mocker: MockerFixture, module_path):
    from kutil.pytest import get_module_patch_fixture
    return get_module_patch_fixture(mocker, module_path)
