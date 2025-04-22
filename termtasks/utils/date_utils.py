"""
Date and calendar utility functions.
"""

import calendar
from datetime import datetime, timedelta
from typing import List


def month_name(month: int) -> str:
    """Get the name of a month.

    Args:
        month: Month number (1-12)

    Returns:
        Month name
    """
    return datetime(2000, month, 1).strftime("%B").upper()


def get_month_calendar(year: int, month: int) -> List[List[int]]:
    """Get calendar representation of a month.

    Args:
        year: Year
        month: Month (1-12)

    Returns:
        List of weeks, where each week is a list of days (0 for days not in month)
    """
    cal = calendar.monthcalendar(year, month)
    return cal


def days_in_month(year: int, month: int) -> int:
    """Get the number of days in a month.

    Args:
        year: Year
        month: Month (1-12)

    Returns:
        Number of days in the month
    """
    return calendar.monthrange(year, month)[1]


def next_month(date: datetime) -> datetime:
    """Get the first day of the next month.

    Args:
        date: Current date

    Returns:
        Date representing the first day of the next month
    """
    if date.month == 12:
        return datetime(date.year + 1, 1, 1)
    else:
        return datetime(date.year, date.month + 1, 1)


def prev_month(date: datetime) -> datetime:
    """Get the first day of the previous month.

    Args:
        date: Current date

    Returns:
        Date representing the first day of the previous month
    """
    if date.month == 1:
        return datetime(date.year - 1, 12, 1)
    else:
        return datetime(date.year, date.month - 1, 1)


def format_date_for_display(date: datetime) -> str:
    """Format a date for display.

    Args:
        date: Date to format

    Returns:
        Formatted date string
    """
    return date.strftime("%Y-%m-%d")


def format_time_for_display(date: datetime) -> str:
    """Format a time for display.

    Args:
        date: Date/time to format

    Returns:
        Formatted time string
    """
    return date.strftime("%H:%M")


def parse_date_time(date_str: str, time_str: str) -> datetime:
    """Parse date and time strings into a datetime object.

    Args:
        date_str: Date string in YYYY-MM-DD format
        time_str: Time string in HH:MM format

    Returns:
        datetime object

    Raises:
        ValueError: If the date or time string is invalid
    """
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
