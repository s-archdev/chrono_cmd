"""
Task list window component.
"""

import curses
from termtasks.models import TaskList
from termtasks.ui.window import Window


class TaskListWindow(Window):
    """Window for displaying the task list."""

    def __init__(self, height: int, width: int, y: int, x: int):
        """Initialize the task list window."""
        super().__init__(height, width, y, x, "TASK LIST")

    def update(self, task_list: TaskList, selected_index: int, active: bool = False) -> None:
        """Update the task list display.

        Args:
            task_list: The task list to display
            selected_index: Index of the selected task
            active: Whether this window is active
        """
        self.win.clear()
        self.draw_border(active)

        if not task_list.tasks:
            content_h, content_w = self.get_content_dims()
            message = "No tasks scheduled"
            x = (content_w - len(message)) // 2
            self.win.addstr(content_h // 2, x + 1, message)
            return

        # Display tasks
        for i, task in enumerate(task_list.tasks):
            # Skip if out of view
            if i >= self.height - 2:
                break

            # Determine display attributes
            attr = 0
            if i == selected_index and active:
                attr = curses.color_pair(2)
            elif task.completed:
                attr = curses.color_pair(3)

            # Format task
            check = "☑" if task.completed else "☐"
            task_str = f"{check} {task.start_str} {task.title}"

            # Truncate if needed
            if len(task_str) > self.width - 4:
                task_str = task_str[:self.width - 7] + "..."

            # Display the task
            self.win.addstr(i + 1, 2, task_str, attr)
