#!/usr/bin/env python3

"""
Main entry point for the TermTasks application.
"""

from termtasks.app import TaskSchedulerApp

def main():
    """Run the TermTasks application."""
    app = TaskSchedulerApp()
    app.run()

if __name__ == "__main__":
    main()
