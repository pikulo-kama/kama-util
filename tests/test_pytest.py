from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture


class TestPytest:

    def test_safe_patch_success(self, mocker: MockerFixture):
        """
        Verifies _safe_patch returns the result of a successful patch.
        """

        from kutil.pytest import safe_patch

        mock_patch = mocker.MagicMock(return_value="success")
        result = safe_patch(mock_patch, "os.path.exists", True)

        assert result == "success"
        mock_patch.assert_called_once_with("os.path.exists", True)

    def test_safe_patch_attribute_error(self, mocker: MockerFixture):
        """
        Verifies _safe_patch returns a MagicMock when AttributeError occurs.
        """

        from kutil.pytest import safe_patch

        mock_patch_fn = mocker.MagicMock(side_effect=AttributeError("Missing"))

        result = safe_patch(mock_patch_fn, "invalid.path")

        assert isinstance(result, MagicMock)

    def test_safe_patch_fixture(self, mocker: MockerFixture):

        from kutil.pytest import safe_patch_fixture

        mocker_mock = mocker.MagicMock()
        safe_patch = safe_patch_fixture(mocker_mock)

        result = safe_patch("test", 1, 2, a="b", c="d")

        assert result == mocker_mock.patch.return_value
        mocker_mock.patch.assert_called_once_with("test", 1, 2, a="b", c="d")

    def test_safe_module_patch_fixture(self, mocker: MockerFixture):

        from kutil.pytest import safe_module_patch_fixture

        get_module_patch_mock = mocker.MagicMock()
        safe_module_patch = safe_module_patch_fixture(get_module_patch_mock)

        result = safe_module_patch("test", 1, 2, a="b", c="d")

        assert result == get_module_patch_mock.return_value
        get_module_patch_mock.assert_called_once_with("test", 1, 2, a="b", c="d")

    def test_module_path_resolution(self, mocker: MockerFixture):
        """
        Verifies the string transformation from 'tests.sub.test_file' to 'root.sub.file'.
        """

        from kutil.pytest import module_path_fixture

        # Mocking the pytest FixtureRequest object
        mock_request = mocker.MagicMock()
        mock_request.module.__name__ = "utils.test_date"

        pytest_config_mock = mocker.MagicMock()
        get_plugin_mock = pytest_config_mock.pluginmanager.get_plugin
        get_plugin_mock.return_value.cov_controller.cov.config.source = ["kutil"]

        # Get the inner function
        module_path = module_path_fixture(mock_request, pytest_config_mock)

        # 1. Standard test file
        get_plugin_mock.assert_called_once_with("_cov")
        assert module_path == "kutil.utils.date"

        # 2. Test file for __init__.py (test_init.py)
        mock_request.module.__name__ = "test_init"
        module_path_init = module_path_fixture(mock_request, pytest_config_mock)
        assert module_path_init == "kutil"

    def test_module_path_without_cov_plugin(self, mocker: MockerFixture):

        from kutil.pytest import module_path_fixture

        # Mocking the pytest FixtureRequest object
        mock_request = mocker.MagicMock()
        mock_request.module.__name__ = "utils.test_date"

        pytest_config_mock = mocker.MagicMock()
        get_plugin_mock = pytest_config_mock.pluginmanager.get_plugin
        get_plugin_mock.return_value.cov_controller.cov = None

        with pytest.raises(RuntimeError):
            module_path_fixture(mock_request, pytest_config_mock)

        get_plugin_mock.return_value.cov_controller = None

        with pytest.raises(RuntimeError):
            module_path_fixture(mock_request, pytest_config_mock)

        get_plugin_mock.return_value = None

        with pytest.raises(RuntimeError):
            module_path_fixture(mock_request, pytest_config_mock)

    def test_get_module_patch_integration(self, mocker: MockerFixture):
        """
        Verifies that the factory correctly combines the path and calls mocker.patch.
        """

        from kutil.pytest import module_patch_fixture

        mock_mocker = mocker.MagicMock()
        patcher = module_patch_fixture(mock_mocker, "kutil.process")

        # Perform the patch
        patcher("os.getpid", return_value=123)

        # Check if mocker.patch was called with the correct concatenated string
        mock_mocker.patch.assert_called_once_with("kutil.process.os.getpid", return_value=123)
