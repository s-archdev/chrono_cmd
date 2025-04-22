"""
Storage utilities for TermTasks.
"""

import json
import os
from pathlib import Path
from typing import Dict, List

from termtasks.models import Task, TaskList


class TaskStorage:
    """Handles storing and retrieving tasks."""

    def __init__(self, filepath: str = None):
        """Initialize the storage handler.

        Args:
            filepath: Path to the task storage file. If None, uses default location.
        """
        if filepath is None:
            # Use default location: ~/.termtasks/tasks.json
            home_dir = os.path.expanduser("~")
            data_dir = os.path.join(home_dir, ".termtasks")
            os.makedirs(data_dir, exist_ok=True)
            self.filepath = os.path.join(data_dir, "tasks.json")
        else:
            self.filepath = filepath

    def load_tasks(self) -> TaskList:
        """Load tasks from storage.

        Returns:
            TaskList object containing stored tasks
        """
        task_list = TaskList()

        if not os.path.exists(self.filepath):
            return task_list

        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                for task_data in data["tasks"]:
                    task = Task.from_dict(task_data)
                    task_list.tasks.append(task)
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            # Return empty task list if there's an error
            pass

        task_list.sort_tasks()
        return task_list

    def save_tasks(self, task_list: TaskList) -> None:
        """Save tasks to storage.

        Args:
            task_list: TaskList object containing tasks to save
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        # Convert tasks to dictionary
        data = {
            "tasks": [task.to_dict() for task in task_list.tasks]
        }

        # Write to file
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)
