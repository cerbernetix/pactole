"""Utilities related to days of the week and lottery draw days."""

from __future__ import annotations

import datetime
from datetime import date
from enum import Enum
from typing import Iterable

WEEK = 7
(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY) = range(WEEK)
DAY_NAMES = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
NAMES_TO_WEEKDAY = {name: i for i, name in enumerate(DAY_NAMES)}

Day = int | float | str | date


class Weekday(Enum):
    """Enumeration for the days of the week.

    It provides utility methods to navigate and calculate differences between weekdays.

    Args:
        value (Day | Weekday | None): The day as an integer (0=Monday, 6=Sunday), a Weekday,
            a timestamp, or a date. If the day is None, the day of the current date is used.

            Integers are converted to Weekday. A Weekday enumeration can also be provided directly.
            A timestamp can be provided as a float representing seconds since the epoch.
            When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
            Both timestamp and string inputs are converted to date objects.
            Date objects will be converted to the corresponding weekday.

            Defaults to None.

    Raises:
            TypeError: If the provided day is not an integer, Weekday, or date.

    Examples:
        >>> Weekday(0)
        Weekday.MONDAY
        >>> Weekday("2023-03-15")
        Weekday.WEDNESDAY
        >>> Weekday(datetime.date(2023, 3, 15))
        Weekday.WEDNESDAY
        >>> Weekday.today()
        Weekday.<CURRENT_DAY>
        >>> Weekday(None)
        Weekday.<CURRENT_DAY>
        >>> Weekday.WEDNESDAY.next()
        Weekday.THURSDAY
        >>> Weekday.WEDNESDAY.until(Weekday.FRIDAY)
        2
        >>> Weekday.FRIDAY.next_date("2023-03-15")
        datetime.date(2023, 3, 17)
    """

    MONDAY = MONDAY
    TUESDAY = TUESDAY
    WEDNESDAY = WEDNESDAY
    THURSDAY = THURSDAY
    FRIDAY = FRIDAY
    SATURDAY = SATURDAY
    SUNDAY = SUNDAY

    @classmethod
    def _missing_(cls, value: Day | Weekday | None = None) -> None:
        """Create Weekday from various input types."""
        if value is None:
            value = datetime.date.today()
        elif isinstance(value, str):
            day_lower = value.strip().lower()
            if day_lower in NAMES_TO_WEEKDAY:
                value = NAMES_TO_WEEKDAY[day_lower]
            else:
                value = datetime.date.fromisoformat(value)
        elif isinstance(value, float):
            value = datetime.date.fromtimestamp(value)

        if isinstance(value, date):
            return cls(value.weekday())

        if isinstance(value, int):
            return cls(value % WEEK)

        return super()._missing_(value)

    def next(self, days: Day | Weekday | Iterable[Day | Weekday] | None = None) -> Weekday:
        """Get a Weekday representing the next day of the week.

        Args:
            days (Day | Weekday | Iterable[Day | Weekday] | None, optional): The target day(s) as
                an integer (0=Monday, 6=Sunday), a Weekday, a timestamp, or a date. Accepts multiple
                days as an iterable.

                When None is provided, simply returns the next day of the week. Otherwise, finds the
                next occurrence among the provided days.

                Integers are converted to Weekday. A Weekday enumeration can also be provided.
                A timestamp can be provided as a float representing seconds since the epoch.
                When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
                Both timestamp and string inputs are converted to date objects.
                Date objects will be converted to the corresponding weekday.

                Defaults to None.

        Returns:
            Weekday: A Weekday enumeration representing the next day of the week.

        Raises:
            TypeError: If the provided day is not an integer, Weekday, or date.

        Examples:
            >>> today = Weekday.WEDNESDAY
            >>> today.next()
            Weekday.THURSDAY
            >>> today.next(Weekday.MONDAY)
            Weekday.MONDAY
            >>> today.next([Weekday.FRIDAY, Weekday.SUNDAY])
            Weekday.FRIDAY
        """
        if days is None:
            next_value = (self.value + 1) % WEEK
            return Weekday(next_value)

        if not isinstance(days, Iterable) or isinstance(days, (str, date)):
            days = [days]
        days = sorted(self.get_day(day).value for day in days)

        for day in days:
            if day > self.value:
                return Weekday(day)
        return Weekday(days[0])

    def previous(self, days: Day | Weekday | Iterable[Day | Weekday] | None = None) -> Weekday:
        """Get a Weekday representing the previous day of the week.

        Args:
            days (Day | Weekday | Iterable[Day | Weekday] | None, optional): The target day(s) as
                an integer (0=Monday, 6=Sunday), a Weekday, a timestamp, or a date. Accepts multiple
                days as an iterable.

                When None is provided, simply returns the previous day of the week. Otherwise, finds
                the previous occurrence among the provided days.

                Integers are converted to Weekday. A Weekday enumeration can also be provided.
                A timestamp can be provided as a float representing seconds since the epoch.
                When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
                Both timestamp and string inputs are converted to date objects.
                Date objects will be converted to the corresponding weekday.

                Defaults to None.

        Returns:
            Weekday: A Weekday enumeration representing the previous day of the week.

        Raises:
            TypeError: If the provided day is not an integer, Weekday, or date.

        Examples:
            >>> today = Weekday.WEDNESDAY
            >>> today.previous()
            Weekday.TUESDAY
            >>> today.previous(Weekday.MONDAY)
            Weekday.MONDAY
            >>> today.previous([Weekday.FRIDAY, Weekday.SUNDAY])
            Weekday.SUNDAY
        """
        if days is None:
            previous_value = (self.value - 1) % WEEK
            return Weekday(previous_value)

        if not isinstance(days, Iterable) or isinstance(days, (str, date)):
            days = [days]
        days = sorted(self.get_day(day).value for day in days)

        for day in reversed(days):
            if day < self.value:
                return Weekday(day)
        return Weekday(days[-1])

    def until(self, day: Day | Weekday | None = None) -> int:
        """Get the number of days until the next occurrence of a given weekday.

        If no target day is provided, the day of the current date is used.

        Args:
            day (Day | Weekday | None, optional): The target day as an integer (0=Monday, 6=Sunday),
                a Weekday, a timestamp, or a date.

                Integers are converted to Weekday. A Weekday enumeration can also be provided.
                A timestamp can be provided as a float representing seconds since the epoch.
                When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
                Both timestamp and string inputs are converted to date objects.
                Date objects will be converted to the corresponding weekday.

                Defaults to None.

        Returns:
            int: The number of days until the next occurrence of the target weekday.

        Raises:
            TypeError: If the provided day is not an integer, Weekday, or date.

        Examples:
            >>> today = Weekday.WEDNESDAY
            >>> today.until(Weekday.FRIDAY)
            2
            >>> today.until(Weekday.MONDAY)
            5
            >>> today.until(Weekday.WEDNESDAY)
            7
        """
        day = self.get_day(day)
        return (day.value + WEEK - self.value - 1) % WEEK + 1

    def since(self, day: Day | Weekday | None = None) -> int:
        """Get the number of days since the previous occurrence of a given weekday.

        If no target day is provided, the day of the current date is used.

        Args:
            day (Day | Weekday | None, optional): The target day as an integer (0=Monday, 6=Sunday),
                a Weekday, a timestamp, or a date.

                Integers are converted to Weekday. A Weekday enumeration can also be provided.
                A timestamp can be provided as a float representing seconds since the epoch.
                When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
                Both timestamp and string inputs are converted to date objects.
                Date objects will be converted to the corresponding weekday.

                Defaults to None.

        Returns:
            int: The number of days since the previous occurrence of the target weekday.

        Raises:
            TypeError: If the provided day is not an integer, Weekday, or date.

        Examples:
            >>> today = Weekday.WEDNESDAY
            >>> today.since(Weekday.MONDAY)
            2
            >>> today.since(Weekday.FRIDAY)
            5
            >>> today.since(Weekday.WEDNESDAY)
            7
        ```
        """
        day = self.get_day(day)
        return (WEEK - day.value + self.value - 1) % WEEK + 1

    def closest(self, day: Day | Weekday | None = None) -> int:
        """Get the number of days to the closest occurrence of a given weekday.

        If no target day is provided, the day of the current date is used.

        Args:
            day (Day | Weekday | None, optional): The target day as an integer (0=Monday, 6=Sunday),
                a Weekday, a timestamp, or a date.

                Integers are converted to Weekday. A Weekday enumeration can also be provided.
                A timestamp can be provided as a float representing seconds since the epoch.
                When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
                Both timestamp and string inputs are converted to date objects.
                Date objects will be converted to the corresponding weekday.

                Defaults to None.

        Returns:
            int: The number of days to the closest occurrence of the target weekday.

        Raises:
            TypeError: If the provided day is not an integer, Weekday, or date.

        Examples:
            >>> today = Weekday.WEDNESDAY
            >>> today.closest(Weekday.FRIDAY)
            2
            >>> today.closest(Weekday.MONDAY)
            -2
            >>> today.closest(Weekday.WEDNESDAY)
            0
        """
        day = self.get_day(day)

        if self == day:
            return 0

        until = self.until(day)
        since = self.since(day)

        return until if until <= since else -since

    def furthest(self, day: Day | Weekday | None = None) -> int:
        """Get the number of days to the furthest occurrence of a given weekday from this day.

        If no target day is provided, the day of the current date is used.

        Args:
            day (Day | Weekday | None, optional): The target day as an integer (0=Monday, 6=Sunday),
                a Weekday, a timestamp, or a date.

                Integers are converted to Weekday. A Weekday enumeration can also be provided.
                A timestamp can be provided as a float representing seconds since the epoch.
                When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
                Both timestamp and string inputs are converted to date objects.
                Date objects will be converted to the corresponding weekday.

                Defaults to None.

        Returns:
            int: The number of days to the furthest occurrence of the target weekday.

        Raises:
            TypeError: If the provided day is not an integer, Weekday, or date.

        Examples:
            >>> today = Weekday.WEDNESDAY
            >>> today.furthest(Weekday.FRIDAY)
            -5
            >>> today.furthest(Weekday.MONDAY)
            5
            >>> today.furthest(Weekday.WEDNESDAY)
            7
        """
        day = self.get_day(day)

        if self == day:
            return WEEK

        until = self.until(day)
        since = self.since(day)

        return until if until > since else -since

    def next_date(self, from_date: Day | None = None, closest: bool = False) -> date:
        """Get the next date for this weekday from a given date.

        If no date is provided, the current date is used.

        Args:
            from_date (Day | None, optional): The starting date.

                A timestamp can be provided as an integer or float representing
                seconds since the epoch. When a string is provided, it must be in the ISO format
                'YYYY-MM-DD'. Finally, a date object can be provided directly.

                Defaults to None.
            closest (bool): If True, get the closest date (past or future). Defaults to False.

        Returns:
            date: The next date for this weekday.

        Raises:
            TypeError: If the provided date is not a string, timestamp, or date object.
            ValueError: If the string is not a valid date in ISO format.

        Examples:
            >>> today = datetime.date(2023, 3, 15)
            >>> Weekday.FRIDAY.next_date(today)
            datetime.date(2023, 3, 17)
            >>> Weekday.MONDAY.next_date(today)
            datetime.date(2023, 3, 20)
            >>> Weekday.WEDNESDAY.next_date(today)
            datetime.date(2023, 3, 22)
            >>> Weekday.WEDNESDAY.next_date(today, closest=True)
            datetime.date(2023, 3, 15)
        """
        from_date = self.get_date(from_date)
        weekday = self.get_day(from_date)

        if closest and weekday == self:
            return from_date

        delta = weekday.until(self)
        return from_date + datetime.timedelta(days=delta)

    def previous_date(self, from_date: Day | None = None, closest: bool = False) -> date:
        """Get the previous date for this weekday from a given date.

        If no date is provided, the current date is used.

        Args:
            from_date (Day | None, optional): The starting date.

                A timestamp can be provided as an integer or float representing
                seconds since the epoch. When a string is provided, it must be in the ISO format
                'YYYY-MM-DD'. Finally, a date object can be provided directly.

                Defaults to None.
            closest (bool): If True, get the closest date (past or future). Defaults to False.

        Returns:
            date: The previous date for this weekday.

        Raises:
            TypeError: If the provided date is not a string, timestamp, or date object.
            ValueError: If the string is not a valid date in ISO format.

        Examples:
            >>> today = datetime.date(2023, 3, 15)
            >>> Weekday.MONDAY.previous_date(today)
            datetime.date(2023, 3, 13)
            >>> Weekday.FRIDAY.previous_date(today)
            datetime.date(2023, 3, 10)
            >>> Weekday.WEDNESDAY.previous_date(today)
            datetime.date(2023, 3, 8)
            >>> Weekday.WEDNESDAY.previous_date(today, closest=True)
            datetime.date(2023, 3, 15)
        """
        from_date = self.get_date(from_date)
        weekday = self.get_day(from_date)

        if closest and weekday == self:
            return from_date

        delta = weekday.since(self)
        return from_date - datetime.timedelta(days=delta)

    def closest_date(self, from_date: Day | None = None) -> date:
        """Get the closest date for this weekday from a given date.

        If no date is provided, the current date is used.

        Args:
            from_date (Day | None, optional): The starting date.

                A timestamp can be provided as an integer or float representing
                seconds since the epoch. When a string is provided, it must be in the ISO format
                'YYYY-MM-DD'. Finally, a date object can be provided directly.

                Defaults to None.

        Returns:
            date: The closest date for this weekday.

        Raises:
            TypeError: If the provided date is not a string, timestamp, or date object.
            ValueError: If the string is not a valid date in ISO format.

        Examples:
            >>> today = datetime.date(2023, 3, 15)
            >>> Weekday.FRIDAY.closest_date(today)
            datetime.date(2023, 3, 17)
            >>> Weekday.MONDAY.closest_date(today)
            datetime.date(2023, 3, 13)
            >>> Weekday.WEDNESDAY.closest_date(today)
            datetime.date(2023, 3, 15)
        """
        from_date = self.get_date(from_date)
        weekday = self.get_day(from_date)

        if weekday == self:
            return from_date

        delta = weekday.closest(self)
        return from_date + datetime.timedelta(days=delta)

    def furthest_date(self, from_date: Day | None = None) -> date:
        """Get the furthest date for this weekday from a given date.

        If no date is provided, the current date is used.

        Args:
            from_date (Day | None, optional): The starting date.

                A timestamp can be provided as an integer or float representing
                seconds since the epoch. When a string is provided, it must be in the ISO format
                'YYYY-MM-DD'. Finally, a date object can be provided directly.

                Defaults to None.

        Returns:
            date: The furthest date for this weekday.

        Raises:
            TypeError: If the provided date is not a string, timestamp, or date object.
            ValueError: If the string is not a valid date in ISO format.

        Examples:
            >>> today = datetime.date(2023, 3, 15)
            >>> Weekday.FRIDAY.furthest_date(today)
            datetime.date(2023, 3, 10)
            >>> Weekday.MONDAY.furthest_date(today)
            datetime.date(2023, 3, 20)
            >>> Weekday.WEDNESDAY.furthest_date(today)
            datetime.date(2023, 3, 22)
        """
        from_date = self.get_date(from_date)
        weekday = self.get_day(from_date)

        if weekday == self:
            return from_date + datetime.timedelta(days=WEEK)

        delta = weekday.furthest(self)
        return from_date + datetime.timedelta(days=delta)

    @classmethod
    def today(cls) -> Weekday:
        """Get the current day of the week, as a Weekday enumeration.

        Returns:
            Weekday: A Weekday enumeration representing the current day of the week.

        Examples:
            >>> Weekday.today()
            Weekday.<CURRENT_DAY>
        """
        return cls(datetime.date.today().weekday())

    @classmethod
    def get_day(cls, day: Day | Weekday | None = None) -> Weekday:
        """Get the Weekday enumeration from an integer.

        If the day is None, the day of the current date is returned.

        Args:
            day (Day | Weekday | None): The day as an integer (0=Monday, 6=Sunday), a Weekday,
                a timestamp, or a date.

                A Weekday enumeration can be provided directly, in which case it is
                returned as is. Integers are converted to Weekday.

                A timestamp can be provided as a float representing seconds since the epoch.
                When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
                Both timestamp and string inputs are converted to date objects.
                Date objects will be converted to the corresponding weekday.

                Defaults to None.

        Returns:
            Weekday: The corresponding Weekday enumeration.

        Raises:
            TypeError: If the provided day is not an integer, Weekday, or date.

        Examples:
            >>> Weekday.get_day()
            Weekday.<CURRENT_DAY>
            >>> Weekday.get_day(2)
            Weekday.WEDNESDAY
            >>> Weekday.get_day(Weekday.FRIDAY)
            Weekday.FRIDAY
            >>> Weekday.get_day("2023-03-15")
            Weekday.WEDNESDAY
            >>> Weekday.get_day("Tuesday")
            Weekday.TUESDAY
            >>> Weekday.get_day("April")
            Raises TypeError
        """
        if isinstance(day, Weekday):
            return day

        if isinstance(day, int):
            return cls(day % WEEK)

        if isinstance(day, str):
            day_lower = day.strip().lower()
            if day_lower in NAMES_TO_WEEKDAY:
                return cls(NAMES_TO_WEEKDAY[day_lower])

        if not isinstance(day, date):
            day = cls.get_date(day)

        return cls(day.weekday())

    @staticmethod
    def get_date(from_date: Day | None = None) -> date:
        """Get the date from a string, timestamp, or a date object.

        If the date is None, the current date is returned.

        Args:
            from_date (Day | None, optional): The date as a string in ISO format, a timestamp,
                or a date object.

                A timestamp can be provided as an integer or float representing
                seconds since the epoch.

                When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.

                Finally, a date object can be provided directly, in which case it is returned as is.

                Defaults to None.

        Returns:
            date: The corresponding date object.

        Raises:
            TypeError: If the provided date is not a string, timestamp, or date object.
            ValueError: If the string is not a valid date in ISO format.

        Examples:
            >>> Weekday.get_date()
            datetime.date(<CURRENT_YEAR>, <CURRENT_MONTH>, <CURRENT_DAY>)
            >>> Weekday.get_date("2023-03-15")
            datetime.date(2023, 3, 15)
            >>> Weekday.get_date(datetime.date(2023, 3, 15))
            datetime.date(2023, 3, 15)
            >>> Weekday.get_date(1678838400)
            datetime.date(2023, 3, 15)
            >>> Weekday.get_date("15-03-2023")
            Raises ValueError
        """
        if from_date is None:
            return datetime.date.today()

        if isinstance(from_date, (int, float)):
            return datetime.date.fromtimestamp(from_date)

        if isinstance(from_date, str):
            return datetime.date.fromisoformat(from_date)

        if not isinstance(from_date, date):
            raise TypeError(
                "The date must be a date object, a string in ISO format, or a timestamp."
            )

        return from_date


class DrawDays:
    """Utility class to handle lottery draw days.

    Args:
        days (Iterable[Day | Weekday]): An iterable of Day or Weekday representing draw days.

    Examples:
        >>> draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])
        >>> draw_days.get_last_draw_date(date(2024, 6, 5))
        datetime.date(2024, 6, 3)
        >>> draw_days.get_next_draw_date(date(2024, 6, 5))
        datetime.date(2024, 6, 6)
    """

    _days: tuple[Weekday, ...]

    def __init__(self, days: Iterable[Day | Weekday]) -> None:
        self._days = tuple(Weekday.get_day(day) for day in days)

    @property
    def days(self) -> tuple[Weekday, ...]:
        """Return the draw days.

        Returns:
            tuple[Weekday, ...]: The draw days.

        Examples:
            >>> draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])
            >>> draw_days.days
            (Weekday.MONDAY, Weekday.THURSDAY)
        """
        return self._days

    def get_last_draw_date(
        self,
        from_date: Day | Weekday | None = None,
        closest: bool = True,
    ) -> date:
        """Return the date of the last lottery draw.

        Args:
            from_date (Day | Weekday | None, optional): The starting date.

                A timestamp can be provided as an integer or float representing
                seconds since the epoch. When a string is provided, it must be in the ISO format
                'YYYY-MM-DD'. Finally, a date object can be provided directly.

                Defaults to None.

        Returns:
            date: The date of the last lottery draw.

        Raises:
            TypeError: If the provided date is not a string, timestamp, or date object.
            ValueError: If the string is not a valid date in ISO format.

        Examples:
            >>> draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])
            >>> draw_days.get_last_draw_date(date(2024, 6, 5))
            datetime.date(2024, 6, 3)
        """
        day = Weekday.get_day(from_date)
        if not closest or day not in self._days:
            day = day.previous(self._days)
        return day.previous_date(from_date, closest=closest)

    def get_next_draw_date(
        self,
        from_date: Day | Weekday | None = None,
        closest: bool = True,
    ) -> date:
        """Return the date of the next lottery draw.

        Args:
            from_date (Day | Weekday | None, optional): The starting date.

                A timestamp can be provided as an integer or float representing
                seconds since the epoch. When a string is provided, it must be in the ISO format
                'YYYY-MM-DD'. Finally, a date object can be provided directly.

                Defaults to None.

        Returns:
            date: The date of the next lottery draw.

        Raises:
            TypeError: If the provided date is not a string, timestamp, or date object.
            ValueError: If the string is not a valid date in ISO format.

        Examples:
            >>> draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])
            >>> draw_days.get_next_draw_date(date(2024, 6, 5))
            datetime.date(2024, 6, 6)
        """
        day = Weekday.get_day(from_date)
        if not closest or day not in self._days:
            day = day.next(self._days)
        return day.next_date(from_date, closest=closest)
