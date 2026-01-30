import requests


class TestRequestUtil:

    def test_success(self, module_patch, save_file_mock):
        """
        Verify True is returned when download and save succeed.
        """

        from kutil.request import url_retrieve

        get_mock = module_patch("requests.get")
        get_mock.return_value.content = b"sample_data"
        get_mock.return_value.status_code = 200

        assert url_retrieve("https://test.com/file.png", "path/to/file.png") is True
        get_mock.assert_called_once_with("https://test.com/file.png", timeout=10)
        save_file_mock.assert_called_once_with("path/to/file.png", b"sample_data", binary=True)

    def test_network_failure(self, module_patch):
        """
        Verify False is returned on request exceptions (e.g., ConnectionError).
        """

        from kutil.request import url_retrieve

        module_patch("requests.get", side_effect=requests.exceptions.ConnectionError)

        assert url_retrieve("https://test.com/bad-url", "path/to/file.png") is False

    def test_http_status_error(self, module_patch):
        """
        Verify False is returned if the server returns a 4xx or 5xx error.
        """

        from kutil.request import url_retrieve

        get_mock = module_patch("requests.get")
        get_mock.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()

        assert url_retrieve("https://test.com/404", "path/to/file.png") is False

    def test_timeout(self, module_patch):
        """
        Verify False is returned when the request times out.
        """

        from kutil.request import url_retrieve

        module_patch("requests.get", side_effect=requests.exceptions.Timeout)

        result = url_retrieve("https://test.com/slow", "path/to/file.png")

        assert result is False