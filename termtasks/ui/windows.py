"""
Base window class for TermTasks UI.
"""

import curses
from typing import Tuple


class Window:
    """Base class for UI windows."""

    def __init__(self, height: int, width: int, y: int, x: int, title: str = ""):
        """Initialize a window.

        Args:
            height: Window height
            width: Window width
            y: Y position (row)
            x: X position (column)
            title: Window title
        """
        self.height = height
        self.width = width
        self.y = y
        self.x = x
        self.title = title
        self.win = curses.newwin(height, width, y, x)
        self.win.keypad(True)

    def draw_border(self, active: bool = False) -> None:
        """Draw a border around the window.

        Args:
            active: Whether this is the active window
        """
        attr = curses.A_BOLD if active else 0
        self.win.attron(attr)
        self.win.box()
        self.win.attroff(attr)

        # Draw title if provided
        if self.title:
            title_x = (self.width - len(self.title) - 4) // 2
            if title_x < 1:
                title_x = 1
            self.win.addstr(0, title_x, f" {self.title} ", attr)

    def get_content_dims(self) -> Tuple[int, int]:
        """Get dimensions for the content area (inside border)."""
        return self.height - 2, self.width - 2

    def clear(self) -> None:
        """Clear the window."""
        self.win.clear()

    def refresh(self) -> None:
        """Refresh the window."""
        self.win.refresh()

    def resize(self, height: int, width: int, y: int, x: int) -> None:
        """Resize and reposition the window.

        Args:
            height: New height
            width: New width
            y: New Y position
            x: New X position
        """
        self.height = height
        self.width = width
        self.y = y
        self.x = x
        self.win.resize(height, width)
        self.win.mvwin(y, x)
