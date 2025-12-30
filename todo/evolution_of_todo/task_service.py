"""Task service for the todo application.

This module provides the TaskService class that encapsulates
business logic for task operations with validation.

References:
- T006: Create task_service.py with create_task() method
- T009: Add validation for empty title
- T011: Add list_tasks() method
- T015: Add update_task() method
- T018: Add delete_task() method
- T021: Add complete_task() and incomplete_task() methods
"""

from typing import Optional
from .task import Task
from .task_storage import TaskStorage


class TaskService:
    """Orchestrates task operations with business logic and validation.

    Acts as a layer between the menu controller and task storage,
    handling validation and error cases.

    Attributes:
        storage: The TaskStorage instance for data operations
    """

    # Validation constraints
    MIN_TITLE_LENGTH = 1
    MAX_TITLE_LENGTH = 200
    MAX_DESCRIPTION_LENGTH = 1000

    def __init__(self, storage: TaskStorage) -> None:
        """Initialize the service with task storage.

        Args:
            storage: TaskStorage instance for data operations
        """
        self._storage = storage

    def create_task(
        self,
        title: str,
        description: Optional[str] = None
    ) -> Task:
        """Create a new task with validation.

        Args:
            title: Task title (1-200 characters)
            description: Optional task description

        Returns:
            The created Task object

        Raises:
            ValueError: If title is empty or too long
        """
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty")
        if len(title) > self.MAX_TITLE_LENGTH:
            raise ValueError(
                f"Title must be {self.MAX_TITLE_LENGTH} characters or less"
            )

        if description is not None:
            description = description.strip()
            if len(description) > self.MAX_DESCRIPTION_LENGTH:
                description = description[:self.MAX_DESCRIPTION_LENGTH]

        task = Task(title=title, description=description)
        return self._storage.add_task(task)

    def list_tasks(self) -> list[Task]:
        """Retrieve all tasks.

        Returns:
            List of all tasks in insertion order
        """
        return self._storage.get_all_tasks()

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> bool:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            True if updated successfully, False if task not found

        Raises:
            ValueError: If title is empty or too long
        """
        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Title cannot be empty")
            if len(title) > self.MAX_TITLE_LENGTH:
                raise ValueError(
                    f"Title must be {self.MAX_TITLE_LENGTH} characters or less"
                )

        if description is not None:
            description = description.strip()
            if len(description) > self.MAX_DESCRIPTION_LENGTH:
                description = description[:self.MAX_DESCRIPTION_LENGTH]

        return self._storage.update_task(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if deleted, False if not found
        """
        return self._storage.delete_task(task_id)

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as complete.

        Args:
            task_id: The ID of the task to complete

        Returns:
            True if marked complete, False if not found
        """
        return self._storage.mark_complete(task_id)

    def incomplete_task(self, task_id: int) -> bool:
        """Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark incomplete

        Returns:
            True if marked incomplete, False if not found
        """
        return self._storage.mark_incomplete(task_id)

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID.

        Args:
            task_id: The ID of the task

        Returns:
            Task if found, None otherwise
        """
        return self._storage.get_task(task_id)
