"""
Task entry window component.
"""

import curses
from datetime import datetime
from typing import Optional

from termtasks.models import Task
from termtasks.ui.window import Window


class TaskEntryWindow(Window):
    """Window for entering new tasks."""

    def __init__(self, height: int, width: int, y: int, x: int):
        """Initialize the task entry window."""
        super().__init__(height, width, y, x, "TASK ENTRY")

    def update(self) -> None:
        """Update the task entry display."""
        self.win.clear()
        self.draw_border()

        # Display task entry form
        self.win.addstr(2, 2, "Task: _")
        self.win.addstr(3, 2, "Date (YYYY-MM-DD): ____-__-__")
        self.win.addstr(4, 2, "Start time (HH:MM): __:__")
        self.win.addstr(5, 2, "End time (HH:MM): __:__ (optional)")

        # Display shortcuts
        self.win.addstr(7, 2, "[a]dd task  [c]omplete task  [q]uit")

    def prompt_for_task(self, stdscr) -> Optional[Task]:
        """Prompt the user for task details.

        Args:
            stdscr: The main curses screen

        Returns:
            Task object or None if cancelled
        """
        curses.echo()
        curses.curs_set(1)  # Show cursor

        # Get task title
        self.win.addstr(2, 2, "Task: ")
        self.win.clrtoeol()
        title = self.win.getstr(2, 8, 40).decode('utf-8')
        if not title:
            curses.noecho()
            curses.curs_set(0)  # Hide cursor
            return None

        # Get date
        today = datetime.now()
        default_date = today.strftime("%Y-%m-%d")
        self.win.addstr(3, 2, f"Date (YYYY-MM-DD) [{default_date}]: ")
        self.win.clrtoeol()
        date_str = self.win.getstr(3, 30, 10).decode('utf-8')
        if not date_str:
            date_str = default_date

        # Get start time
        default_time = today.strftime("%H:%M")
        self.win.addstr(4, 2, f"Start time (HH:MM) [{default_time}]: ")
        self.win.clrtoeol()
        start_time_str = self.win.getstr(4, 32, 5).decode('utf-8')
        if not start_time_str:
            start_time_str = default_time

        # Get end time (optional)
        self.win.addstr(5, 2, "End time (HH:MM) [optional]: ")
        self.win.clrtoeol()
        end_time_str = self.win.getstr(5, 32, 5).decode('utf-8')

        # Reset cursor state
        curses.noecho()
        curses.curs_set(0)  # Hide cursor

        try:
            # Parse datetime
            start_datetime = datetime.strptime(f"{date_str} {start_time_str}", "%Y-%m-%d %H:%M")
            end_datetime = None
            if end_time_str:
                end_datetime = datetime.strptime(f"{date_str} {end_time_str}", "%Y-%m-%d %H:%M")

            # Create task
            return Task(
                title=title,
                start_time=start_datetime,
                end_time=end_datetime,
                completed=False
            )
        except ValueError:
            # Display error message
            self.win.addstr(6, 2, "Invalid date/time format!", curses.A_BOLD)
            self.win.refresh()
            stdscr.getch()  # Wait for key press
            return None
