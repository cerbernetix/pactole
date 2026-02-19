"""Unit tests for the DrawDays class."""

from datetime import date

from pactole.utils import DrawDays, Weekday

DATE_1_MONDAY = date(2024, 6, 3)
DATE_1_TUESDAY = date(2024, 6, 4)
DATE_1_WEDNESDAY = date(2024, 6, 5)
DATE_1_THURSDAY = date(2024, 6, 6)
DATE_1_FRIDAY = date(2024, 6, 7)
DATE_1_SATURDAY = date(2024, 6, 8)
DATE_1_SUNDAY = date(2024, 6, 9)

DATE_2_MONDAY = date(2024, 6, 10)
DATE_2_TUESDAY = date(2024, 6, 11)
DATE_2_WEDNESDAY = date(2024, 6, 12)
DATE_2_THURSDAY = date(2024, 6, 13)
DATE_2_FRIDAY = date(2024, 6, 14)
DATE_2_SATURDAY = date(2024, 6, 15)
DATE_2_SUNDAY = date(2024, 6, 16)

DATE_3_MONDAY = date(2024, 6, 17)
DATE_3_TUESDAY = date(2024, 6, 18)
DATE_3_WEDNESDAY = date(2024, 6, 19)
DATE_3_THURSDAY = date(2024, 6, 20)
DATE_3_FRIDAY = date(2024, 6, 21)
DATE_3_SATURDAY = date(2024, 6, 22)
DATE_3_SUNDAY = date(2024, 6, 23)


class TestDrawDays:
    """Tests for the DrawDays class."""

    def test_draw_days_from_values(self):
        """Test the initialization of DrawDays from values."""
        days = DrawDays([Weekday.MONDAY, Weekday.WEDNESDAY, Weekday.FRIDAY])
        assert days.days == (Weekday.MONDAY, Weekday.WEDNESDAY, Weekday.FRIDAY)

    def test_draw_days_get_last_draw_date(self):
        """Test the get_last_draw_date method."""
        days = DrawDays([Weekday.TUESDAY, Weekday.FRIDAY])

        assert days.get_last_draw_date(from_date=DATE_2_MONDAY, closest=False) == DATE_1_FRIDAY
        assert days.get_last_draw_date(from_date=DATE_2_TUESDAY, closest=False) == DATE_1_FRIDAY
        assert days.get_last_draw_date(from_date=DATE_2_WEDNESDAY, closest=False) == DATE_2_TUESDAY
        assert days.get_last_draw_date(from_date=DATE_2_THURSDAY, closest=False) == DATE_2_TUESDAY
        assert days.get_last_draw_date(from_date=DATE_2_FRIDAY, closest=False) == DATE_2_TUESDAY
        assert days.get_last_draw_date(from_date=DATE_2_SATURDAY, closest=False) == DATE_2_FRIDAY
        assert days.get_last_draw_date(from_date=DATE_2_SUNDAY, closest=False) == DATE_2_FRIDAY

        assert days.get_last_draw_date(from_date=DATE_2_MONDAY, closest=True) == DATE_1_FRIDAY
        assert days.get_last_draw_date(from_date=DATE_2_TUESDAY, closest=True) == DATE_2_TUESDAY
        assert days.get_last_draw_date(from_date=DATE_2_WEDNESDAY, closest=True) == DATE_2_TUESDAY
        assert days.get_last_draw_date(from_date=DATE_2_THURSDAY, closest=True) == DATE_2_TUESDAY
        assert days.get_last_draw_date(from_date=DATE_2_FRIDAY, closest=True) == DATE_2_FRIDAY
        assert days.get_last_draw_date(from_date=DATE_2_SATURDAY, closest=True) == DATE_2_FRIDAY
        assert days.get_last_draw_date(from_date=DATE_2_SUNDAY, closest=True) == DATE_2_FRIDAY

    def test_draw_days_get_next_draw_date(self):
        """Test the get_next_draw_date method."""
        days = DrawDays([Weekday.TUESDAY, Weekday.FRIDAY])

        assert days.get_next_draw_date(from_date=DATE_2_MONDAY, closest=False) == DATE_2_TUESDAY
        assert days.get_next_draw_date(from_date=DATE_2_TUESDAY, closest=False) == DATE_2_FRIDAY
        assert days.get_next_draw_date(from_date=DATE_2_WEDNESDAY, closest=False) == DATE_2_FRIDAY
        assert days.get_next_draw_date(from_date=DATE_2_THURSDAY, closest=False) == DATE_2_FRIDAY
        assert days.get_next_draw_date(from_date=DATE_2_FRIDAY, closest=False) == DATE_3_TUESDAY
        assert days.get_next_draw_date(from_date=DATE_2_SATURDAY, closest=False) == DATE_3_TUESDAY
        assert days.get_next_draw_date(from_date=DATE_2_SUNDAY, closest=False) == DATE_3_TUESDAY

        assert days.get_next_draw_date(from_date=DATE_2_MONDAY, closest=True) == DATE_2_TUESDAY
        assert days.get_next_draw_date(from_date=DATE_2_TUESDAY, closest=True) == DATE_2_TUESDAY
        assert days.get_next_draw_date(from_date=DATE_2_WEDNESDAY, closest=True) == DATE_2_FRIDAY
        assert days.get_next_draw_date(from_date=DATE_2_THURSDAY, closest=True) == DATE_2_FRIDAY
        assert days.get_next_draw_date(from_date=DATE_2_FRIDAY, closest=True) == DATE_2_FRIDAY
        assert days.get_next_draw_date(from_date=DATE_2_SATURDAY, closest=True) == DATE_3_TUESDAY
        assert days.get_next_draw_date(from_date=DATE_2_SUNDAY, closest=True) == DATE_3_TUESDAY
