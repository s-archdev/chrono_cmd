"""
Calendar window component.
"""

import calendar
import curses
from datetime import datetime, timedelta

from termtasks.models import TaskList
from termtasks.ui.window import Window
from termtasks.utils.date_utils import get_month_calendar, month_name


class CalendarWindow(Window):
    """Window for displaying the calendar view."""

    def __init__(self, height: int, width: int, y: int, x: int):
        """Initialize the calendar window."""
        super().__init__(height, width, y, x)

    def update(self, current_date: datetime, task_list: TaskList, active: bool = False) -> None:
        """Update the calendar display.

        Args:
            current_date: The current date to display
            task_list: The task list to display tasks from
            active: Whether this window is active
        """
        self.win.clear()
        self.title = f"CALENDAR - {month_name(current_date.month)} {current_date.year}"
        self.draw_border(active)

        content_h, content_w = self.get_content_dims()
        
        # Display day headers
        day_header = "   MON  TUE  WED  THU  FRI  SAT  SUN  "
        self.win.addstr(1, (content_w - len(day_header)) // 2 + 1, day_header)
        
        # Get calendar for current month
        cal = get_month_calendar(current_date.year, current_date.month)
        
        # Display calendar
        row = 2
        for week in cal:
            cal_line = "  "
            for day in week:
                if day == 0:
                    cal_line += "     "
                else:
                    # Check if there are tasks for this day
                    day_date = current_date.replace(day=day)
                    tasks_today = task_list.get_tasks_for_date(day_date)
                    
                    # Highlight today's date
                    today = datetime.now().date()
                    is_today = day_date.date() == today
                    
                    # Format the day number
                    if is_today:
                        day_str = f"{day:2d}*"
                    elif tasks_today:
                        day_str = f"{day:2d}."
                    else:
                        day_str = f"{day:2d} "
                    
                    # Add spacing
                    cal_line += f" {day_str}  "
            
            # Display the calendar line
            self.win.addstr(row, (content_w - len(cal_line)) // 2 + 1, cal_line)
            row += 1
            
            # Break if we've run out of space
            if row >= content_h - 6:
                break
        
        # Display tasks for today
        today = datetime.now()
        tasks_today = task_list.get_tasks_for_date(today)
        
        row += 1
        self.win.addstr(row, 2, f"* Today: {len(tasks_today)} tasks")
        
        # List today's tasks
        for i, task in enumerate(tasks_today):
            if row + i + 1 >= content_h:
                break
                
            task_display = f"  - {task.title} ({task.start_time.strftime('%H:%M')})"
            if len(task_display) > content_w - 2:
                task_display = task_display[:content_w - 5] + "..."
                
            self.win.addstr(row + i + 1, 2, task_display)
        
        # Display navigation help
        nav_help = "Navigation: [p]rev month  [n]ext month"
        self.win.addstr(content_h - 2, 2, nav_help)
