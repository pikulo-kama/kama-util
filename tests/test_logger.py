import logging
from unittest.mock import call

import pytest
from pytest_mock import MockerFixture


class TestLogger:

    @pytest.fixture(scope="module", autouse=True)
    def _setup_module(self):
        """
        Patches external dependencies (constants, file util) and system arguments
        before the module is imported to correctly set initial globals.
        """

        import kutil.logger as module
        module._log_file_name = "my_service"

        return module


    @pytest.fixture
    def _logging_mock(self, module_patch):
        return module_patch("logging")


    @pytest.fixture
    def _file_handler_mock(self, module_patch):
        return module_patch("TimedRotatingFileHandler")

    @pytest.fixture
    def _logger_module(self, _setup_module):
        """
        Resets the module's global state (_logback, _initialized) and root logger
        handlers before each test for isolation.
        """

        module = _setup_module

        # Reset module globals
        module._logback = {}
        module._initialized = False

        # Clear handlers from the root logger for consistent testing of initialize_logging
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        yield module

    @pytest.mark.parametrize("log_name, configured_level, expected_level", [
        ("com.app.worker", "DEBUG", logging.DEBUG),
        ("com.app.api", "WARN", logging.WARN),
        ("com.app.disabled", "OFF", "OFF"),
    ])
    def test_get_log_level_configured(self, _logger_module, log_name, configured_level, expected_level):
        """
        Tests getting a log level configured in logback.
        """

        # Mock _get_logback to return a configuration including the test level
        mock_logback = {log_name: configured_level, "ROOT": "INFO"}

        level = _logger_module._get_log_level(log_name, mock_logback)

        assert level == expected_level


    def test_get_log_level_default(self, _logger_module):
        """
        Tests falling back to the default level (logging.INFO).
        """

        level = _logger_module._get_log_level(
            "un_configured.logger",
            {"com.other.app": "DEBUG"}
        )

        assert level == logging.INFO


    def test_initialize_logging_first_call(self, module_patch, _logger_module, _logging_mock, _file_handler_mock,
                                           path_exists_mock, path_join_mock, read_file_mock):
        """
        Tests that logging is initialized correctly on the first call, setting up the root logger.
        """

        logback_path = "/path/to/logback"
        logback = {"com.test.file": "INFO"}

        module_patch("logging.Formatter")
        read_file_mock.return_value = logback

        assert len(_logger_module._logback) == 0

        _logger_module.initialize_logging("target", logback_path)

        read_file_mock.assert_called_once_with(logback_path, as_json=True)
        assert _logger_module._logback == logback

        # 1. Check TimedRotatingFileHandler creation
        _file_handler_mock.assert_called_once_with(
            "target/my_service.log",
            when="midnight",
            interval=1,
            backupCount=5,
            encoding="utf-8"
        )

        # 2. Check handler configuration (suffix and formatter)
        assert _file_handler_mock.return_value.suffix == "%Y-%m-%d.log"
        _file_handler_mock.return_value.setFormatter.assert_called()

        _logging_mock.getLogger.return_value.addHandler.assert_called_with(_file_handler_mock.return_value)

    def test_initialize_logging_removes_handlers(self, mocker: MockerFixture, _logger_module, _logging_mock,
                                                 read_file_mock, _file_handler_mock):

        root_logger = _logging_mock.getLogger.return_value
        handler1 = mocker.MagicMock()
        handler2 = mocker.MagicMock()

        root_logger.handlers = [handler1, handler2]

        _logger_module.initialize_logging("target", "path")

        root_logger.removeHandler.assert_has_calls([
            call(handler1),
            call(handler2),
        ])

        handler1.close.assert_called_once()
        handler2.close.assert_called_once()


    def test_get_logger_level_configured(self, _logger_module, mocker, _logging_mock):
        """
        Tests logger returned with a specific, non-OFF log level.
        """

        mock_logger = _logging_mock.getLogger.return_value
        mock_logger.disabled = False

        mocker.patch.object(_logger_module, "initialize_logging")
        mocker.patch.object(_logger_module, "_get_log_level", return_value=logging.DEBUG)

        logger = _logger_module.get_logger("test_logger_debug")

        assert logger is mock_logger
        _logging_mock.getLogger.assert_called_with("test_logger_debug")
        mock_logger.setLevel.assert_called_once_with(logging.DEBUG)
        assert mock_logger.disabled is False


    def test_get_logger_level_off(self, _logging_mock, _logger_module, mocker):
        """
        Tests logger returned with 'OFF' level is disabled.
        """

        mocker.patch.object(_logger_module, 'initialize_logging')
        mocker.patch.object(_logger_module, '_get_log_level', return_value=_logger_module.OFF_LOG_LEVEL)

        logger = _logger_module.get_logger("test_logger_off")
        get_logger_mock = _logging_mock.getLogger.return_value

        assert logger is get_logger_mock
        _logging_mock.getLogger.assert_called_with("test_logger_off")
        get_logger_mock.setLevel.assert_not_called()
        assert get_logger_mock.disabled is True
