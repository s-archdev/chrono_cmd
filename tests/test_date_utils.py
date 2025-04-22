"""
Tests for date utility functions.
"""

import unittest
from datetime import datetime

from termtasks.utils.date_utils import (
    month_name,
    get_month_calendar,
    days_in_month,
    next_month,
    prev_month,
    format_date_for_display,
    format_time_for_display,
    parse_date_time,
)


class TestDateUtils(unittest.TestCase):
    """Test the date utility functions."""

    def test_month_name(self):
        """Test getting month names."""
        self.assertEqual(month_name(1), "JANUARY")
        self.assertEqual(month_name(4), "APRIL")
        self.assertEqual(month_name(12), "DECEMBER")

    def test_get_month_calendar(self):
        """Test getting calendar representation."""
        # Test April 2025 - First day is Tuesday
        cal = get_month_calendar(2025, 4)
        
        # Check first week (partial)
        self.assertEqual(cal[0][0], 0)  # Monday is empty
        self.assertEqual(cal[0][1], 1)  # Tuesday is 1st
        
        # Check number of weeks
        self.assertGreaterEqual(len(cal), 4)
        self.assertLessEqual(len(cal), 6)
        
        # Check that each week has 7 days
        for week in cal:
            self.assertEqual(len(week), 7)

    def test_days_in_month(self):
        """Test getting number of days in a month."""
        self.assertEqual(days_in_month(2025, 1), 31)  # January
        self.assertEqual(days_in_month(2025, 2), 28)  # February (non-leap year)
        self.assertEqual(days_in_month(2024, 2), 29)  # February (leap year)
        self.assertEqual(days_in_month(2025, 4), 30)  # April

    def test_next_month(self):
        """Test getting the next month."""
        # Regular month
        date = datetime(2025, 4, 15)
        next_date = next_month(date)
        self.assertEqual(next_date.year, 2025)
        self.assertEqual(next_date.month, 5)
        self.assertEqual(next_date.day, 1)
        
        # December -> January
        date = datetime(2025, 12, 25)
        next_date = next_month(date)
        self.assertEqual(next_date.year, 2026)
        self.assertEqual(next_date.month, 1)
        self.assertEqual(next_date.day, 1)

    def test_prev_month(self):
        """Test getting the previous month."""
        # Regular month
        date = datetime(2025, 4, 15)
        prev_date = prev_month(date)
        self.assertEqual(prev_date.year, 2025)
        self.assertEqual(prev_date.month, 3)
        self.assertEqual(prev_date.day, 1)
        
        # January -> December
        date = datetime(2025, 1, 15)
        prev_date = prev_month(date)
        self.assertEqual(prev_date.year, 2024)
        self.assertEqual(prev_date.month, 12)
        self.assertEqual(prev_date.day, 1)

    def test_format_date_for_display(self):
        """Test formatting dates for display."""
        date = datetime(2025, 4, 22)
        self.assertEqual(format_date_for_display(date), "2025-04-22")

    def test_format_time_for_display(self):
        """Test formatting times for display."""
        time = datetime(2025, 4, 22, 9, 30)
        self.assertEqual(format_time_for_display(time), "09:30")

    def test_parse_date_time(self):
        """Test parsing date and time strings."""
        date_str = "2025-04-22"
        time_str = "09:30"
        dt = parse_date_time(date_str, time_str)
        
        self.assertEqual(dt.year, 2025)
        self.assertEqual(dt.month, 4)
        self.assertEqual(dt.day, 22)
        self.assertEqual(dt.hour, 9)
        self.assertEqual(dt.minute, 30)
        
        # Test invalid format
        with self.assertRaises(ValueError):
            parse_date_time("04/22/2025", "9:30 AM")


if __name__ == "__main__":
    unittest.main()
