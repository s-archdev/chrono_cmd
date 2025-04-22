"""
Main application controller for TermTasks.
"""

import curses
import locale
import sys
from datetime import datetime

from termtasks.models import Task, TaskList
from termtasks.ui.window import Window
from termtasks.ui.task_list import TaskListWindow
from termtasks.ui.calendar import CalendarWindow
from termtasks.ui.task_entry import TaskEntryWindow
from termtasks.utils.storage import TaskStorage

class TaskSchedulerApp:
    """Main application controller for the task scheduler."""

    def __init__(self):
        """Initialize the application."""
        self.task_storage = TaskStorage()
        self.task_list = self.task_storage.load_tasks()
        self.current_date = datetime.now()
        self.selected_task_index = 0
        self.active_panel = 0  # 0: task list, 1: calendar

    def run(self):
        """Run the application main loop."""
        # Set up locale for proper display of dates and times
        locale.setlocale(locale.LC_ALL, '')

        # Initialize curses
        curses.wrapper(self._main_loop)

    def _main_loop(self, stdscr):
        """Main application loop with curses screen."""
        # Hide cursor
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        
        # Initialize color pairs
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Header
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected
        curses.init_pair(3, curses.COLOR_GREEN, -1)  # Completed tasks
        curses.init_pair(4, curses.COLOR_YELLOW, -1)  # Today
        curses.init_pair(5, curses.COLOR_CYAN, -1)  # Highlight
        
        # Get screen dimensions
        height, width = stdscr.getmaxyx()
        half_width = width // 2

        # Create windows
        task_list_win = TaskListWindow(height - 10, half_width, 0, 0)
        task_entry_win = TaskEntryWindow(10, half_width, height - 10, 0)
        calendar_win = CalendarWindow(height, width - half_width, 0, half_width)
        
        # Main loop
        while True:
            # Clear screen
            stdscr.clear()
            
            # Update task list and calendar windows
            task_list_win.update(self.task_list, self.selected_task_index, self.active_panel == 0)
            calendar_win.update(self.current_date, self.task_list, self.active_panel == 1)
            task_entry_win.update()
            
            # Refresh all windows
            stdscr.refresh()
            task_list_win.refresh()
            calendar_win.refresh()
            task_entry_win.refresh()
            
            # Get key press
            key = stdscr.getch()
            
            # Handle key press
            if key == ord('q'):  # Quit
                break
            elif key == ord('a'):  # Add task
                new_task = task_entry_win.prompt_for_task(stdscr)
                if new_task:
                    self.task_list.add_task(new_task)
                    self.task_storage.save_tasks(self.task_list)
            elif key == ord('c'):  # Complete task
                if self.task_list.tasks and 0 <= self.selected_task_index < len(self.task_list.tasks):
                    task = self.task_list.tasks[self.selected_task_index]
                    task.completed = not task.completed
                    self.task_storage.save_tasks(self.task_list)
            elif key == ord('j'):  # Down
                if self.active_panel == 0 and self.task_list.tasks:
                    self.selected_task_index = (self.selected_task_index + 1) % len(self.task_list.tasks)
            elif key == ord('k'):  # Up
                if self.active_panel == 0 and self.task_list.tasks:
                    self.selected_task_index = (self.selected_task_index - 1) % len(self.task_list.tasks)
            elif key == ord('n'):  # Next month
                if self.active_panel == 1:
                    month = self.current_date.month
                    year = self.current_date.year
                    if month == 12:
                        month = 1
                        year += 1
                    else:
                        month += 1
                    self.current_date = self.current_date.replace(year=year, month=month, day=1)
            elif key == ord('p'):  # Previous month
                if self.active_panel == 1:
                    month = self.current_date.month
                    year = self.current_date.year
                    if month == 1:
                        month = 12
                        year -= 1
                    else:
                        month -= 1
                    self.current_date = self.current_date.replace(year=year, month=month, day=1)
            elif key == 9:  # Tab key - switch panels
                self.active_panel = (self.active_panel + 1) % 2
