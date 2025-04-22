"""
Data models for TermTasks.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Task:
    """Represents a scheduled task."""

    title: str
    start_time: datetime
    end_time: Optional[datetime] = None
    completed: bool = False
    id: Optional[str] = None

    def __post_init__(self):
        """Initialize the task ID if not provided."""
        if self.id is None:
            self.id = f"{self.start_time.strftime('%Y%m%d%H%M%S')}"

    @property
    def start_str(self) -> str:
        """Return a string representation of the start time."""
        return self.start_time.strftime("%Y-%m-%d %H:%M")

    @property
    def end_str(self) -> str:
        """Return a string representation of the end time."""
        if self.end_time:
            return self.end_time.strftime("%H:%M")
        return ""

    @property
    def is_all_day(self) -> bool:
        """Return True if the task is an all-day event."""
        return self.start_time.hour == 0 and self.start_time.minute == 0 and self.end_time is None

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "id": self.id,
            "title": self.title,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task from dictionary data."""
        return cls(
            id=data["id"],
            title=data["title"],
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"]) if data["end_time"] else None,
            completed=data["completed"],
        )


@dataclass
class TaskList:
    """A collection of tasks."""

    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the list."""
        self.tasks.append(task)
        self.sort_tasks()

    def remove_task(self, task_id: str) -> None:
        """Remove a task from the list."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_tasks_for_date(self, date: datetime) -> List[Task]:
        """Get all tasks for a specific date."""
        return [
            task for task in self.tasks
            if task.start_time.date() == date.date()
        ]

    def sort_tasks(self) -> None:
        """Sort tasks by start time."""
        self.tasks.sort(key=lambda t: t.start_time)
