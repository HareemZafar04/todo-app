"""Menu controller for the todo application.

This module provides the MenuController class that handles
user input, dispatches actions, and manages the menu loop.

References:
- T008: Create menu.py with _handle_add() method
- T013: Add _handle_view() method
- T016: Add _handle_update() method
- T019: Add _handle_delete() method
- T022: Add _handle_complete() and _handle_incomplete() methods
- T023: Add input validation (numeric check, range check)
- T024: Add task_not_found error handling
- T026: Add error messages for invalid inputs
- T029: Add graceful exit handling
"""

from typing import Optional
from .task_service import TaskService
from .display import Display


class MenuController:
    """Handles user interaction and dispatches actions.

    Manages the menu loop, input validation, and coordinates
    between the task service and display components.

    Attributes:
        service: TaskService for business operations
        display: Display for output formatting
        _running: Whether the menu loop is active
    """

    MIN_OPTION = 1
    MAX_OPTION = 7

    def __init__(self, service: TaskService, display: Optional[Display] = None) -> None:
        """Initialize the menu controller.

        Args:
            service: TaskService for task operations
            display: Display instance (creates default if None)
        """
        self._service = service
        self._display = display or Display()
        self._running = True

    def run(self) -> None:
        """Start the main menu loop."""
        while self._running:
            self._display.show_menu()
            option = self._get_valid_option()
            if option is not None:
                self._dispatch(option)

    def _get_valid_option(self) -> Optional[int]:
        """Get and validate user menu input.

        Returns:
            Valid option number (1-7) or None on error
        """
        while True:
            try:
                user_input = input("Select an option (1-7): ").strip()
                if not user_input:
                    self._display.show_error("Please enter a number between 1 and 7.")
                    continue

                if not user_input.isdigit():
                    self._display.show_error("Please enter a valid number.")
                    continue

                option = int(user_input)
                if option < self.MIN_OPTION or option > self.MAX_OPTION:
                    self._display.show_error(
                        f"Invalid option. Please enter a number between "
                        f"{self.MIN_OPTION} and {self.MAX_OPTION}."
                    )
                    continue

                return option

            except (EOFError, OSError):
                self._display.show_error("Error reading input. Please try again.")

    def _get_valid_task_id(self, prompt: str) -> Optional[int]:
        """Get and validate a task ID input.

        Args:
            prompt: The prompt message for input

        Returns:
            Valid task ID or None if invalid/cancelled
        """
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    return None

                if not user_input.isdigit():
                    self._display.show_error("Please enter a valid number.")
                    continue

                task_id = int(user_input)
                return task_id

            except (EOFError, OSError):
                self._display.show_error("Error reading input. Please try again.")
                return None

    def _dispatch(self, option: int) -> None:
        """Dispatch to the appropriate handler.

        Args:
            option: The menu option number
        """
        handlers = {
            1: self._handle_add,
            2: self._handle_view,
            3: self._handle_update,
            4: self._handle_delete,
            5: self._handle_complete,
            6: self._handle_incomplete,
            7: self._handle_exit,
        }
        handler = handlers.get(option)
        if handler:
            handler()

    def _handle_add(self) -> None:
        """Handle adding a new task."""
        title = input("Enter task title: ").strip()
        if not title:
            self._display.show_error("Title cannot be empty. Please enter a task title.")
            return

        if len(title) > 200:
            self._display.show_error("Title must be 200 characters or less.")
            return

        description = input("Enter description (optional): ").strip()
        if not description:
            description = None

        try:
            task = self._service.create_task(title, description)
            self._display.show_confirmation(f"Task added successfully! (ID: {task.id})")
        except ValueError as e:
            self._display.show_error(str(e))

    def _handle_view(self) -> None:
        """Handle viewing all tasks."""
        tasks = self._service.list_tasks()
        self._display.show_tasks(tasks)

    def _handle_update(self) -> None:
        """Handle updating an existing task."""
        task_id = self._get_valid_task_id("Enter task ID: ")
        if task_id is None:
            return

        task = self._service.get_task(task_id)
        if task is None:
            self._display.show_error(f"Task with ID {task_id} not found.")
            return

        new_title = input(
            f"Enter new title (press Enter to keep '{task.title}'): "
        ).strip()
        if not new_title:
            new_title = task.title

        new_description = input(
            f"Enter new description (press Enter to keep current): "
        ).strip()
        if new_description == "":
            new_description = task.description

        try:
            success = self._service.update_task(
                task_id,
                title=new_title,
                description=new_description
            )
            if success:
                self._display.show_confirmation("Task updated successfully!")
            else:
                self._display.show_error("Failed to update task.")
        except ValueError as e:
            self._display.show_error(str(e))

    def _handle_delete(self) -> None:
        """Handle deleting a task."""
        task_id = self._get_valid_task_id("Enter task ID: ")
        if task_id is None:
            return

        task = self._service.get_task(task_id)
        if task is None:
            self._display.show_error(f"Task with ID {task_id} not found.")
            return

        success = self._service.delete_task(task_id)
        if success:
            self._display.show_confirmation("Task deleted successfully!")
        else:
            self._display.show_error("Failed to delete task.")

    def _handle_complete(self) -> None:
        """Handle marking a task as complete."""
        task_id = self._get_valid_task_id("Enter task ID: ")
        if task_id is None:
            return

        task = self._service.get_task(task_id)
        if task is None:
            self._display.show_error(f"Task with ID {task_id} not found.")
            return

        success = self._service.complete_task(task_id)
        if success:
            self._display.show_confirmation("Task marked as complete!")
        else:
            self._display.show_error("Failed to mark task as complete.")

    def _handle_incomplete(self) -> None:
        """Handle marking a task as incomplete."""
        task_id = self._get_valid_task_id("Enter task ID: ")
        if task_id is None:
            return

        task = self._service.get_task(task_id)
        if task is None:
            self._display.show_error(f"Task with ID {task_id} not found.")
            return

        success = self._service.incomplete_task(task_id)
        if success:
            self._display.show_confirmation("Task marked as incomplete!")
        else:
            self._display.show_error("Failed to mark task as incomplete.")

    def _handle_exit(self) -> None:
        """Handle application exit."""
        self._running = False
        self._display.show_message("Goodbye!")
