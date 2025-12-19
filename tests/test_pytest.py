from unittest.mock import MagicMock
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

    def test_module_path_resolution(self):
        """
        Verifies the string transformation from 'tests.sub.test_file' to 'root.sub.file'.
        """

        from kutil.pytest import module_path_fixture

        # Mocking the pytest FixtureRequest object
        mock_request = MagicMock()
        mock_request.module.__name__ = "utils.test_date"

        # Get the inner function
        get_path_fn = module_path_fixture(mock_request)

        # 1. Standard test file
        assert get_path_fn("kutil") == "kutil.utils.date"

        # 2. Test file for __init__.py (test_init.py)
        mock_request.module.__name__ = "test_init"
        get_path_fn_init = module_path_fixture(mock_request)
        assert get_path_fn_init("kutil") == "kutil"

    def test_get_module_patch_integration(self, mocker: MockerFixture):
        """
        Verifies that the factory correctly combines the path and calls mocker.patch.
        """

        from kutil.pytest import get_module_patch_fixture

        mock_mocker = mocker.MagicMock()
        # Mock the module_path to return a fixed string
        mock_path_resolver = lambda root: f"{root}.process"

        # Get the factory
        factory = get_module_patch_fixture(mock_mocker, mock_path_resolver)

        # Create a patcher for 'kutil'
        patcher = factory("kutil")

        # Perform the patch
        patcher("os.getpid", return_value=123)

        # Check if mocker.patch was called with the correct concatenated string
        mock_mocker.patch.assert_called_once_with("kutil.process.os.getpid", return_value=123)
