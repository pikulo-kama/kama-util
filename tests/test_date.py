from datetime import datetime
import pytest


class TestDateUtil:

    @pytest.fixture
    def format_datetime_mock(self, module_patch):
        return module_patch("format_datetime")

    @pytest.fixture
    def get_localzone_mock(self, module_patch):
        return module_patch("get_localzone")

    def test_string_to_date_conversion(self, get_localzone_mock):
        """
        Tests that string_to_date correctly converts the UTC string
        and localizes it to the mocked local timezone.
        """

        from kutil.date import string_to_date

        string_date = "2024-01-15T10:30:00.000Z"
        expected_tz = "America/New_York"

        get_localzone_mock.return_value = expected_tz
        result_datetime = string_to_date(string_date)

        # 1. Check correct localization to the expected local timezone
        assert str(result_datetime.tzinfo) == expected_tz

        # 2. Check the time shift (10:30 UTC -> 05:30 NY time on Jan 15)
        assert result_datetime.year == 2024
        assert result_datetime.month == 1
        assert result_datetime.day == 15
        assert result_datetime.hour == 5
        assert result_datetime.minute == 30

        # 3. Test an edge case for date change (e.g., midnight UTC)
        string_date_midnight = "2024-01-16T04:00:00.000Z"  # 4:00 UTC = 11:00 PM Jan 15 NY time
        result_midnight = string_to_date(string_date_midnight)
        assert result_midnight.day == 15
        assert result_midnight.hour == 23


    def test_get_verbose_date_with_year(self, format_datetime_mock):
        """
        Tests date formatting when show_year is True.
        """

        from kutil.date import get_verbose_date

        test_datetime = datetime.now()

        get_verbose_date(test_datetime, show_year=True, locale="fr_FR")

        # Check that format_datetime was called with the correct format and locale
        format_datetime_mock.assert_called_once_with(
            test_datetime,
            "d MMMM YYYY",
            locale="fr_FR"
        )

    def test_get_verbose_date_without_year(self, format_datetime_mock):
        """
        Tests date formatting when show_year is False.
        """

        from kutil.date import get_verbose_date

        test_datetime = datetime.now()

        get_verbose_date(test_datetime, show_year=False, locale="de_DE")

        # Check that format_datetime was called with the correct format (excluding year)
        format_datetime_mock.assert_called_once_with(
            test_datetime,
            "d MMMM",
            locale="de_DE"
        )


    def test_get_verbose_time_military_format(self):
        """
        Tests time formatting using the default 24-hour (Military) format.
        """

        from kutil.date import get_verbose_time

        # Test an afternoon time (16:30)
        test_dt = datetime(2024, 1, 15, 16, 30, 0)
        result = get_verbose_time(test_dt, use_military=True)

        assert result == "16:30"

        # Test a morning time (09:05)
        test_dt_morning = datetime(2024, 1, 15, 9, 5, 0)
        result_morning = get_verbose_time(test_dt_morning, use_military=True)
        assert result_morning == "09:05"  # Check for leading zero


    def test_get_verbose_time_regular_format(self):
        """
        Tests time formatting using the 12-hour (Regular) format.
        """

        from kutil.date import get_verbose_time

        # Test an afternoon time (16:30 -> 04:30 PM)
        test_dt_pm = datetime(2024, 1, 15, 16, 30, 0)
        result_pm = get_verbose_time(test_dt_pm, use_military=False)
        assert result_pm == "04:30 PM"

        # Test a morning time (09:05 -> 09:05 AM)
        test_dt_am = datetime(2024, 1, 15, 9, 5, 0)
        result_am = get_verbose_time(test_dt_am, use_military=False)
        assert result_am == "09:05 AM"

        # Test noon (12:00 -> 12:00 PM)
        test_dt_noon = datetime(2024, 1, 15, 12, 0, 0)
        result_noon = get_verbose_time(test_dt_noon, use_military=False)
        assert result_noon == "12:00 PM"

        # Test midnight (00:00 -> 12:00 AM)
        test_dt_midnight = datetime(2024, 1, 15, 0, 0, 0)
        result_midnight = get_verbose_time(test_dt_midnight, use_military=False)
        assert result_midnight == "12:00 AM"
