"""Tests for the Weekday utility."""

import datetime
from unittest import mock

import pytest

from pactole.utils import Weekday


class TestWeekday:
    """Tests for the Weekday utility."""

    def test_weekday_from_today(self):
        """Test creating Weekday from today's date."""

        with mock.patch("pactole.utils.days.datetime.date", wraps=datetime.date) as mock_datetime:
            mock_datetime.today.return_value = datetime.date(2024, 1, 1)

            assert Weekday(None) == Weekday.MONDAY

    def test_weekday_from_invalid_type(self):
        """Test creating Weekday from an invalid type."""

        with pytest.raises(ValueError):
            Weekday({"date": "2024-01-01"})

    def test_weekday_from_int(self):
        """Test creating Weekday from an integer."""

        assert Weekday(7) == Weekday.MONDAY
        assert Weekday(0) == Weekday.MONDAY
        assert Weekday(1) == Weekday.TUESDAY
        assert Weekday(2) == Weekday.WEDNESDAY
        assert Weekday(3) == Weekday.THURSDAY
        assert Weekday(4) == Weekday.FRIDAY
        assert Weekday(5) == Weekday.SATURDAY
        assert Weekday(6) == Weekday.SUNDAY

    def test_weekday_from_weekday(self):
        """Test creating Weekday from a Weekday enum."""

        assert Weekday(Weekday.MONDAY) == Weekday.MONDAY
        assert Weekday(Weekday.TUESDAY) == Weekday.TUESDAY
        assert Weekday(Weekday.WEDNESDAY) == Weekday.WEDNESDAY
        assert Weekday(Weekday.THURSDAY) == Weekday.THURSDAY
        assert Weekday(Weekday.FRIDAY) == Weekday.FRIDAY
        assert Weekday(Weekday.SATURDAY) == Weekday.SATURDAY
        assert Weekday(Weekday.SUNDAY) == Weekday.SUNDAY

    def test_weekday_from_timestamp(self):
        """Test creating Weekday from a float."""

        assert Weekday(datetime.datetime(2024, 1, 1).timestamp()) == Weekday.MONDAY
        assert Weekday(datetime.datetime(2024, 1, 2).timestamp()) == Weekday.TUESDAY
        assert Weekday(datetime.datetime(2024, 1, 3).timestamp()) == Weekday.WEDNESDAY
        assert Weekday(datetime.datetime(2024, 1, 4).timestamp()) == Weekday.THURSDAY
        assert Weekday(datetime.datetime(2024, 1, 5).timestamp()) == Weekday.FRIDAY
        assert Weekday(datetime.datetime(2024, 1, 6).timestamp()) == Weekday.SATURDAY
        assert Weekday(datetime.datetime(2024, 1, 7).timestamp()) == Weekday.SUNDAY

    def test_weekday_from_date(self):
        """Test creating Weekday from a date object."""

        assert Weekday(datetime.date(2024, 1, 1)) == Weekday.MONDAY
        assert Weekday(datetime.date(2024, 1, 2)) == Weekday.TUESDAY
        assert Weekday(datetime.date(2024, 1, 3)) == Weekday.WEDNESDAY
        assert Weekday(datetime.date(2024, 1, 4)) == Weekday.THURSDAY
        assert Weekday(datetime.date(2024, 1, 5)) == Weekday.FRIDAY
        assert Weekday(datetime.date(2024, 1, 6)) == Weekday.SATURDAY
        assert Weekday(datetime.date(2024, 1, 7)) == Weekday.SUNDAY

    def test_weekday_from_string(self):
        """Test creating Weekday from a date string."""

        assert Weekday("2024-01-01") == Weekday.MONDAY
        assert Weekday("2024-01-02") == Weekday.TUESDAY
        assert Weekday("2024-01-03") == Weekday.WEDNESDAY
        assert Weekday("2024-01-04") == Weekday.THURSDAY
        assert Weekday("2024-01-05") == Weekday.FRIDAY
        assert Weekday("2024-01-06") == Weekday.SATURDAY
        assert Weekday("2024-01-07") == Weekday.SUNDAY

    def test_weekday_from_day_name(self):
        """Test creating Weekday from a day name string."""

        assert Weekday("monday") == Weekday.MONDAY
        assert Weekday("tuesday") == Weekday.TUESDAY
        assert Weekday("wednesday") == Weekday.WEDNESDAY
        assert Weekday("thursday") == Weekday.THURSDAY
        assert Weekday("friday") == Weekday.FRIDAY
        assert Weekday("saturday") == Weekday.SATURDAY
        assert Weekday("sunday") == Weekday.SUNDAY

    def test_weekday_from_day_name_case_insensitive(self):
        """Test creating Weekday from a day name string with different cases."""

        assert Weekday("Monday") == Weekday.MONDAY
        assert Weekday("TUESDAY") == Weekday.TUESDAY
        assert Weekday("WeDnEsDaY") == Weekday.WEDNESDAY
        assert Weekday("THURSDAY") == Weekday.THURSDAY
        assert Weekday("Friday") == Weekday.FRIDAY

    def test_weekday_from_day_name_with_spaces(self):
        """Test creating Weekday from a day name string with leading/trailing spaces."""

        assert Weekday("  Monday  ") == Weekday.MONDAY
        assert Weekday("  TUESDAY") == Weekday.TUESDAY
        assert Weekday("WEDNESDAY  ") == Weekday.WEDNESDAY
        assert Weekday("  THURSDAY  ") == Weekday.THURSDAY
        assert Weekday("  Friday") == Weekday.FRIDAY
        assert Weekday("Saturday  ") == Weekday.SATURDAY
        assert Weekday("  Sunday  ") == Weekday.SUNDAY

    def test_weekday_from_invalid_day_name(self):
        """Test creating Weekday from an invalid day name raises ValueError."""

        with pytest.raises(ValueError):
            Weekday("notaday")

    def test_next_weekday_from_current(self):
        """Test the next weekday method."""

        assert Weekday.MONDAY.next() == Weekday.TUESDAY
        assert Weekday.TUESDAY.next() == Weekday.WEDNESDAY
        assert Weekday.WEDNESDAY.next() == Weekday.THURSDAY
        assert Weekday.THURSDAY.next() == Weekday.FRIDAY
        assert Weekday.FRIDAY.next() == Weekday.SATURDAY
        assert Weekday.SATURDAY.next() == Weekday.SUNDAY
        assert Weekday.SUNDAY.next() == Weekday.MONDAY

    def test_next_weekday_from_one(self):
        """Test the next weekday method from one weekday."""

        assert Weekday.MONDAY.next(Weekday.MONDAY) == Weekday.MONDAY
        assert Weekday.FRIDAY.next(Weekday.MONDAY) == Weekday.MONDAY

    def test_next_weekday_from_many(self):
        """Test the next weekday method from many weekdays."""

        assert Weekday.MONDAY.next([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.TUESDAY
        assert Weekday.TUESDAY.next([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.FRIDAY
        assert Weekday.WEDNESDAY.next([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.FRIDAY
        assert Weekday.THURSDAY.next([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.FRIDAY
        assert Weekday.FRIDAY.next([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.TUESDAY
        assert Weekday.SATURDAY.next([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.TUESDAY
        assert Weekday.SUNDAY.next([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.TUESDAY

    def test_previous_weekday_from_current(self):
        """Test the previous weekday method."""

        assert Weekday.MONDAY.previous() == Weekday.SUNDAY
        assert Weekday.TUESDAY.previous() == Weekday.MONDAY
        assert Weekday.WEDNESDAY.previous() == Weekday.TUESDAY
        assert Weekday.THURSDAY.previous() == Weekday.WEDNESDAY
        assert Weekday.FRIDAY.previous() == Weekday.THURSDAY
        assert Weekday.SATURDAY.previous() == Weekday.FRIDAY
        assert Weekday.SUNDAY.previous() == Weekday.SATURDAY

    def test_previous_weekday_from_one(self):
        """Test the previous weekday method from one weekday."""

        assert Weekday.MONDAY.previous(Weekday.MONDAY) == Weekday.MONDAY
        assert Weekday.WEDNESDAY.previous(Weekday.MONDAY) == Weekday.MONDAY

    def test_previous_weekday_from_many(self):
        """Test the previous weekday method from many weekdays."""

        assert Weekday.MONDAY.previous([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.FRIDAY
        assert Weekday.TUESDAY.previous([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.FRIDAY
        assert Weekday.WEDNESDAY.previous([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.TUESDAY
        assert Weekday.THURSDAY.previous([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.TUESDAY
        assert Weekday.FRIDAY.previous([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.TUESDAY
        assert Weekday.SATURDAY.previous([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.FRIDAY
        assert Weekday.SUNDAY.previous([Weekday.TUESDAY, Weekday.FRIDAY]) == Weekday.FRIDAY

    def test_until_day_from_weekday(self):
        """Test the until method with Weekday."""

        assert Weekday.MONDAY.until(Weekday.WEDNESDAY) == 2
        assert Weekday.FRIDAY.until(Weekday.MONDAY) == 3
        assert Weekday.SUNDAY.until(Weekday.SUNDAY) == 7

    def test_until_day_from_num(self):
        """Test the until method with integer day."""

        assert Weekday.WEDNESDAY.until(0) == 5
        assert Weekday.MONDAY.until(4) == 4
        assert Weekday.SUNDAY.until(6) == 7

    def test_until_day_from_timestamp(self):
        """Test the until method with timestamp."""

        assert Weekday.MONDAY.until(datetime.datetime(2024, 1, 3).timestamp()) == 2

    def test_until_day_from_date(self):
        """Test the until method with date."""

        assert Weekday.MONDAY.until(datetime.date(2024, 1, 3)) == 2

    def test_until_day_from_str(self):
        """Test the until method with date string."""

        assert Weekday.MONDAY.until("2024-01-03") == 2

    def test_until_day_from_today(self):
        """Test the until method with today."""

        today = datetime.date(2024, 1, 3)  # Wednesday
        with mock.patch("pactole.utils.days.datetime.date", wraps=datetime.date) as mock_datetime:
            mock_datetime.today.return_value = today
            assert Weekday.MONDAY.until() == 2

    def test_since_day_from_weekday(self):
        """Test the since method with Weekday."""

        assert Weekday.WEDNESDAY.since(Weekday.MONDAY) == 2
        assert Weekday.MONDAY.since(Weekday.FRIDAY) == 3
        assert Weekday.SUNDAY.since(Weekday.SUNDAY) == 7

    def test_since_day_from_num(self):
        """Test the since method with integer day."""

        assert Weekday.WEDNESDAY.since(0) == 2
        assert Weekday.MONDAY.since(4) == 3
        assert Weekday.SUNDAY.since(6) == 7

    def test_since_day_from_timestamp(self):
        """Test the since method with timestamp."""

        assert Weekday.WEDNESDAY.since(datetime.datetime(2024, 1, 1).timestamp()) == 2

    def test_since_day_from_date(self):
        """Test the since method with date."""

        assert Weekday.WEDNESDAY.since(datetime.date(2024, 1, 1)) == 2

    def test_since_day_from_str(self):
        """Test the since method with date string."""

        assert Weekday.WEDNESDAY.since("2024-01-01") == 2

    def test_since_day_from_today(self):
        """Test the since method with today."""

        today = datetime.date(2024, 1, 3)  # Wednesday
        with mock.patch("pactole.utils.days.datetime.date", wraps=datetime.date) as mock_datetime:
            mock_datetime.today.return_value = today
            assert Weekday.MONDAY.since() == 5

    def test_closest_day_from_weekday(self):
        """Test the closest method with Weekday."""

        assert Weekday.MONDAY.closest(Weekday.WEDNESDAY) == 2
        assert Weekday.FRIDAY.closest(Weekday.MONDAY) == 3
        assert Weekday.SUNDAY.closest(Weekday.SUNDAY) == 0

    def test_closest_day_from_num(self):
        """Test the closest method with integer day."""

        assert Weekday.WEDNESDAY.closest(0) == -2
        assert Weekday.MONDAY.closest(4) == -3
        assert Weekday.SUNDAY.closest(6) == 0

    def test_closest_day_from_timestamp(self):
        """Test the closest method with timestamp."""

        assert Weekday.MONDAY.closest(datetime.datetime(2024, 1, 3).timestamp()) == 2

    def test_closest_day_from_date(self):
        """Test the closest method with date."""

        assert Weekday.MONDAY.closest(datetime.date(2024, 1, 3)) == 2

    def test_closest_day_from_str(self):
        """Test the closest method with date string."""

        assert Weekday.MONDAY.closest("2024-01-03") == 2

    def test_closest_day_from_today(self):
        """Test the closest method with today."""

        today = datetime.date(2024, 1, 3)  # Wednesday
        with mock.patch("pactole.utils.days.datetime.date", wraps=datetime.date) as mock_datetime:
            mock_datetime.today.return_value = today
            assert Weekday.MONDAY.closest() == 2

    def test_furthest_day_from_weekday(self):
        """Test the furthest method with Weekday."""

        assert Weekday.MONDAY.furthest(Weekday.WEDNESDAY) == -5
        assert Weekday.FRIDAY.furthest(Weekday.MONDAY) == -4
        assert Weekday.SUNDAY.furthest(Weekday.SUNDAY) == 7

    def test_furthest_day_from_num(self):
        """Test the furthest method with integer day."""

        assert Weekday.WEDNESDAY.furthest(0) == 5
        assert Weekday.MONDAY.furthest(4) == 4
        assert Weekday.SUNDAY.furthest(6) == 7

    def test_furthest_day_from_timestamp(self):
        """Test the furthest method with timestamp."""

        assert Weekday.MONDAY.furthest(datetime.datetime(2024, 1, 3).timestamp()) == -5

    def test_furthest_day_from_date(self):
        """Test the furthest method with date."""

        assert Weekday.MONDAY.furthest(datetime.date(2024, 1, 3)) == -5

    def test_furthest_day_from_str(self):
        """Test the furthest method with date string."""

        assert Weekday.MONDAY.furthest("2024-01-03") == -5

    def test_furthest_day_from_today(self):
        """Test the furthest method with today."""

        today = datetime.date(2024, 1, 3)  # Wednesday
        with mock.patch("pactole.utils.days.datetime.date", wraps=datetime.date) as mock_datetime:
            mock_datetime.today.return_value = today
            assert Weekday.MONDAY.furthest() == -5

    def test_next_date_from_today(self):
        """Test the next_date method with today."""

        today = datetime.date(2024, 1, 3)  # Wednesday
        with mock.patch("pactole.utils.days.datetime.date", wraps=datetime.date) as mock_datetime:
            mock_datetime.today.return_value = today
            assert Weekday.MONDAY.next_date() == datetime.date(2024, 1, 8)

    def test_next_date_from_timestamp(self):
        """Test the next_date method with a timestamp."""

        assert Weekday.MONDAY.next_date(datetime.datetime(2024, 1, 3).timestamp()) == datetime.date(
            2024, 1, 8
        )
        assert Weekday.FRIDAY.next_date(datetime.datetime(2024, 1, 3).timestamp()) == datetime.date(
            2024, 1, 5
        )
        assert Weekday.SUNDAY.next_date(datetime.datetime(2024, 1, 7).timestamp()) == datetime.date(
            2024, 1, 14
        )

        assert Weekday.WEDNESDAY.next_date(
            datetime.datetime(2024, 1, 3).timestamp(), closest=True
        ) == datetime.date(2024, 1, 3)
        assert Weekday.MONDAY.next_date(
            datetime.datetime(2024, 1, 5).timestamp(), closest=True
        ) == datetime.date(2024, 1, 8)
        assert Weekday.SUNDAY.next_date(
            datetime.datetime(2024, 1, 6).timestamp(), closest=True
        ) == datetime.date(2024, 1, 7)

    def test_next_date_from_date(self):
        """Test the next_date method with a date."""

        assert Weekday.MONDAY.next_date(datetime.date(2024, 1, 3)) == datetime.date(2024, 1, 8)
        assert Weekday.FRIDAY.next_date(datetime.date(2024, 1, 3)) == datetime.date(2024, 1, 5)
        assert Weekday.SUNDAY.next_date(datetime.date(2024, 1, 7)) == datetime.date(2024, 1, 14)

        assert Weekday.WEDNESDAY.next_date(
            datetime.date(2024, 1, 3), closest=True
        ) == datetime.date(2024, 1, 3)
        assert Weekday.MONDAY.next_date(datetime.date(2024, 1, 5), closest=True) == datetime.date(
            2024, 1, 8
        )
        assert Weekday.SUNDAY.next_date(datetime.date(2024, 1, 6), closest=True) == datetime.date(
            2024, 1, 7
        )

    def test_next_date_from_str(self):
        """Test the next_date method with a string."""

        assert Weekday.MONDAY.next_date("2024-01-03") == datetime.date(2024, 1, 8)
        assert Weekday.FRIDAY.next_date("2024-01-03") == datetime.date(2024, 1, 5)
        assert Weekday.SUNDAY.next_date("2024-01-07") == datetime.date(2024, 1, 14)

        assert Weekday.WEDNESDAY.next_date("2024-01-03", closest=True) == datetime.date(2024, 1, 3)
        assert Weekday.MONDAY.next_date("2024-01-05", closest=True) == datetime.date(2024, 1, 8)
        assert Weekday.SUNDAY.next_date("2024-01-06", closest=True) == datetime.date(2024, 1, 7)

    def test_previous_date_from_today(self):
        """Test the previous_date method with today."""

        today = datetime.date(2024, 1, 3)  # Wednesday
        with mock.patch("pactole.utils.days.datetime.date", wraps=datetime.date) as mock_datetime:
            mock_datetime.today.return_value = today
            assert Weekday.MONDAY.previous_date() == datetime.date(2024, 1, 1)

    def test_previous_date_from_timestamp(self):
        """Test the previous_date method with a timestamp."""

        assert Weekday.MONDAY.previous_date(
            datetime.datetime(2024, 1, 3).timestamp()
        ) == datetime.date(2024, 1, 1)
        assert Weekday.FRIDAY.previous_date(
            datetime.datetime(2024, 1, 3).timestamp()
        ) == datetime.date(2023, 12, 29)
        assert Weekday.SUNDAY.previous_date(
            datetime.datetime(2024, 1, 7).timestamp()
        ) == datetime.date(2023, 12, 31)

        assert Weekday.WEDNESDAY.previous_date(
            datetime.datetime(2024, 1, 3).timestamp(), closest=True
        ) == datetime.date(2024, 1, 3)
        assert Weekday.MONDAY.previous_date(
            datetime.datetime(2024, 1, 5).timestamp(), closest=True
        ) == datetime.date(2024, 1, 1)
        assert Weekday.SUNDAY.previous_date(
            datetime.datetime(2024, 1, 7).timestamp(), closest=True
        ) == datetime.date(2024, 1, 7)

    def test_previous_date_from_date(self):
        """Test the previous_date method with a date."""

        assert Weekday.MONDAY.previous_date(datetime.date(2024, 1, 3)) == datetime.date(2024, 1, 1)
        assert Weekday.FRIDAY.previous_date(datetime.date(2024, 1, 3)) == datetime.date(
            2023, 12, 29
        )
        assert Weekday.SUNDAY.previous_date(datetime.date(2024, 1, 7)) == datetime.date(
            2023, 12, 31
        )

        assert Weekday.WEDNESDAY.previous_date(
            datetime.date(2024, 1, 3), closest=True
        ) == datetime.date(2024, 1, 3)
        assert Weekday.MONDAY.previous_date(
            datetime.date(2024, 1, 5), closest=True
        ) == datetime.date(2024, 1, 1)
        assert Weekday.SUNDAY.previous_date(
            datetime.date(2024, 1, 7), closest=True
        ) == datetime.date(2024, 1, 7)

    def test_previous_date_from_str(self):
        """Test the previous_date method with a string."""

        assert Weekday.MONDAY.previous_date("2024-01-03") == datetime.date(2024, 1, 1)
        assert Weekday.FRIDAY.previous_date("2024-01-03") == datetime.date(2023, 12, 29)
        assert Weekday.SUNDAY.previous_date("2024-01-07") == datetime.date(2023, 12, 31)

        assert Weekday.WEDNESDAY.previous_date("2024-01-03", closest=True) == datetime.date(
            2024, 1, 3
        )
        assert Weekday.MONDAY.previous_date("2024-01-05", closest=True) == datetime.date(2024, 1, 1)
        assert Weekday.SUNDAY.previous_date("2024-01-07", closest=True) == datetime.date(2024, 1, 7)

    def test_closest_date_from_today(self):
        """Test the closest_date method with today."""

        today = datetime.date(2024, 1, 3)  # Wednesday
        with mock.patch("pactole.utils.days.datetime.date", wraps=datetime.date) as mock_datetime:
            mock_datetime.today.return_value = today
            assert Weekday.MONDAY.closest_date() == datetime.date(2024, 1, 1)

    def test_closest_date_from_timestamp(self):
        """Test the closest_date method with a timestamp."""

        assert Weekday.MONDAY.closest_date(
            datetime.datetime(2024, 1, 3).timestamp()
        ) == datetime.date(2024, 1, 1)
        assert Weekday.FRIDAY.closest_date(
            datetime.datetime(2024, 1, 3).timestamp()
        ) == datetime.date(2024, 1, 5)
        assert Weekday.SUNDAY.closest_date(
            datetime.datetime(2024, 1, 6).timestamp()
        ) == datetime.date(2024, 1, 7)
        assert Weekday.SUNDAY.closest_date(
            datetime.datetime(2024, 1, 7).timestamp()
        ) == datetime.date(2024, 1, 7)

    def test_closest_date_from_date(self):
        """Test the closest_date method with a date."""

        assert Weekday.MONDAY.closest_date(datetime.date(2024, 1, 3)) == datetime.date(2024, 1, 1)
        assert Weekday.FRIDAY.closest_date(datetime.date(2024, 1, 3)) == datetime.date(2024, 1, 5)
        assert Weekday.SUNDAY.closest_date(datetime.date(2024, 1, 6)) == datetime.date(2024, 1, 7)
        assert Weekday.SUNDAY.closest_date(datetime.date(2024, 1, 7)) == datetime.date(2024, 1, 7)

    def test_closest_date_from_str(self):
        """Test the closest_date method with a string."""

        assert Weekday.MONDAY.closest_date("2024-01-03") == datetime.date(2024, 1, 1)
        assert Weekday.FRIDAY.closest_date("2024-01-03") == datetime.date(2024, 1, 5)
        assert Weekday.SUNDAY.closest_date("2024-01-06") == datetime.date(2024, 1, 7)
        assert Weekday.SUNDAY.closest_date("2024-01-07") == datetime.date(2024, 1, 7)

    def test_furthest_date_from_today(self):
        """Test the furthest_date method with today."""

        today = datetime.date(2024, 1, 3)  # Wednesday
        with mock.patch("pactole.utils.days.datetime.date", wraps=datetime.date) as mock_datetime:
            mock_datetime.today.return_value = today
            assert Weekday.MONDAY.furthest_date() == datetime.date(2024, 1, 8)

    def test_furthest_date_from_timestamp(self):
        """Test the furthest_date method with a timestamp."""

        assert Weekday.MONDAY.furthest_date(
            datetime.datetime(2024, 1, 3).timestamp()
        ) == datetime.date(2024, 1, 8)
        assert Weekday.FRIDAY.furthest_date(
            datetime.datetime(2024, 1, 3).timestamp()
        ) == datetime.date(2023, 12, 29)
        assert Weekday.SUNDAY.furthest_date(
            datetime.datetime(2024, 1, 6).timestamp()
        ) == datetime.date(2023, 12, 31)
        assert Weekday.SUNDAY.furthest_date(
            datetime.datetime(2024, 1, 7).timestamp()
        ) == datetime.date(2024, 1, 14)

    def test_furthest_date_from_date(self):
        """Test the furthest_date method with a date."""

        assert Weekday.MONDAY.furthest_date(datetime.date(2024, 1, 3)) == datetime.date(2024, 1, 8)
        assert Weekday.FRIDAY.furthest_date(datetime.date(2024, 1, 3)) == datetime.date(
            2023, 12, 29
        )
        assert Weekday.SUNDAY.furthest_date(datetime.date(2024, 1, 6)) == datetime.date(
            2023, 12, 31
        )
        assert Weekday.SUNDAY.furthest_date(datetime.date(2024, 1, 7)) == datetime.date(2024, 1, 14)

    def test_furthest_date_from_str(self):
        """Test the furthest_date method with a string."""

        assert Weekday.MONDAY.furthest_date("2024-01-03") == datetime.date(2024, 1, 8)
        assert Weekday.FRIDAY.furthest_date("2024-01-03") == datetime.date(2023, 12, 29)
        assert Weekday.SUNDAY.furthest_date("2024-01-06") == datetime.date(2023, 12, 31)
        assert Weekday.SUNDAY.furthest_date("2024-01-07") == datetime.date(2024, 1, 14)

    def test_today(self):
        """Test the today method."""

        with mock.patch("pactole.utils.days.datetime.date", wraps=datetime.date) as mock_datetime:
            mock_datetime.today.return_value = datetime.date(2024, 1, 1)

            assert Weekday.today() == Weekday.MONDAY

    def test_get_day_from_today(self):
        """Test the get_day method with today."""

        with mock.patch("pactole.utils.days.datetime.date", wraps=datetime.date) as mock_datetime:
            mock_datetime.today.return_value = datetime.date(2024, 1, 1)

            assert Weekday.get_day() == Weekday.MONDAY

    def test_get_day_from_num_day(self):
        """Test the get_day method with a numeric day."""

        assert Weekday.get_day(-1) == Weekday.SUNDAY
        assert Weekday.get_day(0) == Weekday.MONDAY
        assert Weekday.get_day(1) == Weekday.TUESDAY
        assert Weekday.get_day(2) == Weekday.WEDNESDAY
        assert Weekday.get_day(3) == Weekday.THURSDAY
        assert Weekday.get_day(4) == Weekday.FRIDAY
        assert Weekday.get_day(5) == Weekday.SATURDAY
        assert Weekday.get_day(6) == Weekday.SUNDAY
        assert Weekday.get_day(7) == Weekday.MONDAY

    def test_get_day_from_weekday(self):
        """Test the get_day method with a Weekday instance."""

        assert Weekday.get_day(Weekday.MONDAY) == Weekday.MONDAY
        assert Weekday.get_day(Weekday.TUESDAY) == Weekday.TUESDAY
        assert Weekday.get_day(Weekday.WEDNESDAY) == Weekday.WEDNESDAY
        assert Weekday.get_day(Weekday.THURSDAY) == Weekday.THURSDAY
        assert Weekday.get_day(Weekday.FRIDAY) == Weekday.FRIDAY
        assert Weekday.get_day(Weekday.SATURDAY) == Weekday.SATURDAY
        assert Weekday.get_day(Weekday.SUNDAY) == Weekday.SUNDAY

    def test_get_day_from_date(self):
        """Test the get_day method with a date."""

        assert Weekday.get_day(datetime.date(2024, 1, 1)) == Weekday.MONDAY
        assert Weekday.get_day(datetime.date(2024, 1, 2)) == Weekday.TUESDAY
        assert Weekday.get_day(datetime.date(2024, 1, 3)) == Weekday.WEDNESDAY
        assert Weekday.get_day(datetime.date(2024, 1, 4)) == Weekday.THURSDAY
        assert Weekday.get_day(datetime.date(2024, 1, 5)) == Weekday.FRIDAY
        assert Weekday.get_day(datetime.date(2024, 1, 6)) == Weekday.SATURDAY
        assert Weekday.get_day(datetime.date(2024, 1, 7)) == Weekday.SUNDAY

    def test_get_day_from_str(self):
        """Test the get_day method with a date string."""

        assert Weekday.get_day("2024-01-01") == Weekday.MONDAY
        assert Weekday.get_day("2024-01-02") == Weekday.TUESDAY
        assert Weekday.get_day("2024-01-03") == Weekday.WEDNESDAY
        assert Weekday.get_day("2024-01-04") == Weekday.THURSDAY
        assert Weekday.get_day("2024-01-05") == Weekday.FRIDAY
        assert Weekday.get_day("2024-01-06") == Weekday.SATURDAY
        assert Weekday.get_day("2024-01-07") == Weekday.SUNDAY

    def test_get_day_from_day_name(self):
        """Test the get_day method with a day name string."""

        assert Weekday.get_day("monday") == Weekday.MONDAY
        assert Weekday.get_day("tuesday") == Weekday.TUESDAY
        assert Weekday.get_day("wednesday") == Weekday.WEDNESDAY
        assert Weekday.get_day("thursday") == Weekday.THURSDAY
        assert Weekday.get_day("friday") == Weekday.FRIDAY
        assert Weekday.get_day("saturday") == Weekday.SATURDAY
        assert Weekday.get_day("sunday") == Weekday.SUNDAY

    def test_get_day_from_day_name_case_insensitive(self):
        """Test the get_day method with day names is case-insensitive."""

        assert Weekday.get_day("Monday") == Weekday.MONDAY
        assert Weekday.get_day("TUESDAY") == Weekday.TUESDAY
        assert Weekday.get_day("WeDnEsDaY") == Weekday.WEDNESDAY

    def test_get_day_from_day_name_with_spaces(self):
        """Test the get_day method with day names with leading/trailing spaces."""

        assert Weekday.get_day("  Monday  ") == Weekday.MONDAY
        assert Weekday.get_day("  TUESDAY") == Weekday.TUESDAY
        assert Weekday.get_day("WEDNESDAY  ") == Weekday.WEDNESDAY
        assert Weekday.get_day("  THURSDAY  ") == Weekday.THURSDAY
        assert Weekday.get_day("  Friday") == Weekday.FRIDAY
        assert Weekday.get_day("Saturday  ") == Weekday.SATURDAY
        assert Weekday.get_day("  Sunday  ") == Weekday.SUNDAY

    def test_get_day_from_invalid_day_name(self):
        """Test the get_day method with an invalid day name raises ValueError."""

        with pytest.raises(ValueError):
            Weekday.get_day("notaday")

    def test_get_date_from_today(self):
        """Test the get_date helper method with today."""

        with mock.patch("pactole.utils.days.datetime.date", wraps=datetime.date) as mock_datetime:
            mock_datetime.today.return_value = datetime.date(2024, 1, 1)

            assert Weekday.get_date() == datetime.date(2024, 1, 1)

    def test_get_date_from_timestamp(self):
        """Test the get_date helper method with a timestamp."""

        assert Weekday.get_date(int(datetime.datetime(2024, 2, 1).timestamp())) == datetime.date(
            2024, 2, 1
        )
        assert Weekday.get_date(datetime.datetime(2024, 1, 1).timestamp()) == datetime.date(
            2024, 1, 1
        )

    def test_get_date_from_str(self):
        """Test the get_date helper method with a string."""

        assert Weekday.get_date("2024-01-01") == datetime.date(2024, 1, 1)

    def test_get_date_from_date(self):
        """Test the get_date helper method with a date."""

        assert Weekday.get_date(datetime.date(2024, 1, 1)) == datetime.date(2024, 1, 1)

    def test_get_date_invalid_type(self):
        """Test the get_date helper method with an invalid type."""

        with pytest.raises(TypeError):
            Weekday.get_date({"date": "2024-01-01"})
