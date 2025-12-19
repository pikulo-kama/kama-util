import pytest
from _pytest.fixtures import FixtureRequest
from pytest_mock import MockerFixture


@pytest.fixture
def safe_patch(mocker: MockerFixture):
    """
    Fixture that provides a safe patching mechanism.

    Returns a functional wrapper that prevents tests from failing if the
    specified patch target does not exist in the current environment.
    """

    from kutil.pytest import safe_patch_fixture
    return safe_patch_fixture(mocker)


@pytest.fixture
def safe_module_patch(get_module_patch):
    """
    Fixture that provides a safe patching mechanism scoped to the source module.

    Wraps the module-level patch factory with error handling to manage
    missing attributes gracefully during the testing lifecycle.
    """

    from kutil.pytest import safe_module_patch_fixture
    return safe_module_patch_fixture(get_module_patch)


@pytest.fixture
def module_path(request: FixtureRequest):
    """
    Fixture that resolves the source module path for the current test file.

    Analyzes the test metadata to automatically determine the package
    structure of the code under test.
    """

    from kutil.pytest import module_path_fixture
    return module_path_fixture(request)


@pytest.fixture
def get_module_patch(mocker: MockerFixture, module_path):
    """
    Fixture that provides a factory for creating module-level mocks.

    Automates the resolution of mock paths by transforming the test
    module's namespace into the corresponding source namespace.
    """

    from kutil.pytest import get_module_patch_fixture
    return get_module_patch_fixture(mocker, module_path)
