"""
Tests for task models.
"""

import unittest
from datetime import datetime

from termtasks.models import Task, TaskList


class TestTask(unittest.TestCase):
    """Test the Task class."""

    def test_init(self):
        """Test Task initialization."""
        # Create a task
        start_time = datetime(2025, 4, 22, 9, 0)
        task = Task("Test Task", start_time)

        # Check attributes
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.start_time, start_time)
        self.assertIsNone(task.end_time)
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.id)

    def test_to_dict(self):
        """Test conversion to dictionary."""
        # Create a task
        start_time = datetime(2025, 4, 22, 9, 0)
        end_time = datetime(2025, 4, 22, 10, 0)
        task = Task("Test Task", start_time, end_time, True, "test-id")

        # Convert to dict
        task_dict = task.to_dict()

        # Check dict values
        self.assertEqual(task_dict["id"], "test-id")
        self.assertEqual(task_dict["title"], "Test Task")
        self.assertEqual(task_dict["start_time"], start_time.isoformat())
        self.assertEqual(task_dict["end_time"], end_time.isoformat())
        self.assertTrue(task_dict["completed"])

    def test_from_dict(self):
        """Test creation from dictionary."""
        # Create a dictionary
        task_dict = {
            "id": "test-id",
            "title": "Test Task",
            "start_time": "2025-04-22T09:00:00",
            "end_time": "2025-04-22T10:00:00",
            "completed": True,
        }

        # Create task from dict
        task = Task.from_dict(task_dict)

        # Check task values
        self.assertEqual(task.id, "test-id")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.start_time, datetime(2025, 4, 22, 9, 0))
        self.assertEqual(task.end_time, datetime(2025, 4, 22, 10, 0))
        self.assertTrue(task.completed)

    def test_is_all_day(self):
        """Test all-day detection."""
        # Create an all-day task
        start_time = datetime(2025, 4, 22, 0, 0)
        task = Task("All Day Task", start_time)
        self.assertTrue(task.is_all_day)

        # Create a regular task
        start_time = datetime(2025, 4, 22, 9, 0)
        task = Task("Regular Task", start_time)
        self.assertFalse(task.is_all_day)


class TestTaskList(unittest.TestCase):
    """Test the TaskList class."""

    def test_add_task(self):
        """Test adding tasks to the list."""
        task_list = TaskList()
        
        # Add a task
        task1 = Task("Task 1", datetime(2025, 4, 22, 9, 0))
        task_list.add_task(task1)
        
        # Check list contents
        self.assertEqual(len(task_list.tasks), 1)
        self.assertEqual(task_list.tasks[0].title, "Task 1")

    def test_remove_task(self):
        """Test removing tasks from the list."""
        task_list = TaskList()
        
        # Add tasks
        task1 = Task("Task 1", datetime(2025, 4, 22, 9, 0), id="task1")
        task2 = Task("Task 2", datetime(2025, 4, 22, 10, 0), id="task2")
        task_list.add_task(task1)
        task_list.add_task(task2)
        
        # Remove a task
        task_list.remove_task("task1")
        
        # Check list contents
        self.assertEqual(len(task_list.tasks), 1)
        self.assertEqual(task_list.tasks[0].id, "task2")

    def test_get_task(self):
        """Test retrieving a task by ID."""
        task_list = TaskList()
        
        # Add tasks
        task1 = Task("Task 1", datetime(2025, 4, 22, 9, 0), id="task1")
        task2 = Task("Task 2", datetime(2025, 4, 22, 10, 0), id="task2")
        task_list.add_task(task1)
        task_list.add_task(task2)
        
        # Get a task
        retrieved_task = task_list.get_task("task2")
        
        # Check task
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.title, "Task 2")
        
        # Try to get a non-existent task
        non_existent_task = task_list.get_task("non-existent")
        self.assertIsNone(non_existent_task)

    def test_get_tasks_for_date(self):
        """Test retrieving tasks for a specific date."""
        task_list = TaskList()
        
        # Add tasks for different dates
        task1 = Task("Task 1", datetime(2025, 4, 22, 9, 0))
        task2 = Task("Task 2", datetime(2025, 4, 22, 15, 0))
        task3 = Task("Task 3", datetime(2025, 4, 23, 10, 0))
        task_list.add_task(task1)
        task_list.add_task(task2)
        task_list.add_task(task3)
        
        # Get tasks for April 22
        apr22_tasks = task_list.get_tasks_for_date(datetime(2025, 4, 22))
        
        # Check tasks
        self.assertEqual(len(apr22_tasks), 2)
        self.assertEqual(apr22_tasks[0].title, "Task 1")
        self.assertEqual(apr22_tasks[1].title, "Task 2")
        
        # Get tasks for April 23
        apr23_tasks = task_list.get_tasks_for_date(datetime(2025, 4, 23))
        
        # Check tasks
        self.assertEqual(len(apr23_tasks), 1)
        self.assertEqual(apr23_tasks[0].title, "Task 3")

    def test_sort_tasks(self):
        """Test sorting tasks by start time."""
        task_list = TaskList()
        
        # Add tasks in random order
        task2 = Task("Task 2", datetime(2025, 4, 22, 10, 0))
        task1 = Task("Task 1", datetime(2025, 4, 22, 9, 0))
        task3 = Task("Task 3", datetime(2025, 4, 23, 9, 0))
        task_list.add_task(task2)
        task_list.add_task(task1)
        task_list.add_task(task3)
        
        # Tasks should be sorted already due to add_task calling sort_tasks
        self.assertEqual(task_list.tasks[0].title, "Task 1")
        self.assertEqual(task_list.tasks[1].title, "Task 2")
        self.assertEqual(task_list.tasks[2].title, "Task 3")


if __name__ == "__main__":
    unittest.main()
