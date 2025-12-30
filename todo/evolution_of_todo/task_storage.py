"""In-memory task storage for the todo application.

This module provides the TaskStorage class that manages
the in-memory list of tasks and handles ID generation.

References:
- T005: Create TaskStorage class in src/task_storage.py
- T010: Add list_tasks() method to TaskStorage
- T014: Add update_task() method to TaskStorage
- T017: Add delete_task() method to TaskStorage
- T020: Add mark_complete() and mark_incomplete() methods
"""

from typing import Optional
from .task import Task


class TaskStorage:
    """Manages in-memory storage of tasks.

    Provides methods for CRUD operations on tasks stored
    in a simple Python list. IDs are auto-incremented.

    Attributes:
        _tasks: List of Task objects (in insertion order)
        _next_id: Next available ID for new tasks (starts at 1)
    """

    def __init__(self) -> None:
        """Initialize empty task storage with first ID set to 1."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, task: Task) -> Task:
        """Add a task to storage and assign it a unique ID.

        Args:
            task: The Task object to add (ID should be 0)

        Returns:
            The added Task with assigned ID
        """
        task.id = self._generate_id()
        self._tasks.append(task)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The Task if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks in insertion order.

        Returns:
            List of all Task objects
        """
        return self._tasks.copy()

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> bool:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (if provided, keeps current if None)
            description: New description (if provided, keeps current if None)

        Returns:
            True if task was found and updated, False otherwise
        """
        task = self.get_task(task_id)
        if task is None:
            return False

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if task was found and deleted, False otherwise
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        return False

    def mark_complete(self, task_id: int) -> bool:
        """Mark a task as complete.

        Args:
            task_id: The ID of the task to mark complete

        Returns:
            True if task was found and updated, False otherwise
        """
        task = self.get_task(task_id)
        if task is None:
            return False
        task.completed = True
        return True

    def mark_incomplete(self, task_id: int) -> bool:
        """Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark incomplete

        Returns:
            True if task was found and updated, False otherwise
        """
        task = self.get_task(task_id)
        if task is None:
            return False
        task.completed = False
        return True

    def _generate_id(self) -> int:
        """Generate the next unique task ID.

        Returns:
            The next available positive integer ID
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id
