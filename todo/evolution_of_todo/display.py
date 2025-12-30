"""Display formatter for the todo application.

This module provides the Display class for formatting and
printing output to the terminal.

References:
- T007: Create display.py with show_menu() and show_confirmation()
- T012: Add show_tasks() and format_task_table() methods
- T025: Add show_message() for empty list
"""

from typing import List
from .task import Task


class Display:
    """Handles all terminal output formatting and display.

    Provides methods for displaying menus, tasks, messages,
    and confirmation notices.

    Attributes:
        None (stateless utility class)
    """

    MENU_WIDTH = 40

    def show_menu(self) -> None:
        """Display the main menu options."""
        print()
        print("=" * self.MENU_WIDTH)
        print("Todo Application")
        print("=" * self.MENU_WIDTH)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Complete")
        print("6. Mark Incomplete")
        print("7. Exit")
        print("=" * self.MENU_WIDTH)
        print()

    def show_tasks(self, tasks: List[Task]) -> None:
        """Display all tasks in a formatted table.

        Args:
            tasks: List of Task objects to display
        """
        if not tasks:
            print("No tasks found. Add a task to get started!")
            return

        # Calculate column widths
        id_width = 5
        title_width = 30
        status_width = 10

        # Header
        print(f"{'ID':<{id_width}} | {'Title':<{title_width}} | {'Status':<{status_width}}")
        print("-" * (id_width + 2 + title_width + 2 + status_width))

        # Rows
        for task in tasks:
            title = task.title[:title_width]
            if len(task.title) > title_width:
                title += "..."

            status = "[x]" if task.completed else "[ ]"

            print(
                f"{task.id:<{id_width}} | "
                f"{title:<{title_width}} | "
                f"{status:<{status_width}}"
            )

            # Show description on next line if present
            if task.description:
                print(f"{'':>{id_width}}   {'  ' + task.description}")

    def show_message(self, message: str) -> None:
        """Display an informational message.

        Args:
            message: The message to display
        """
        print(message)

    def show_confirmation(self, action: str) -> None:
        """Display a confirmation message.

        Args:
            action: Description of the action performed
        """
        print(f"{action}")

    def show_error(self, message: str) -> None:
        """Display an error message.

        Args:
            message: The error message to display
        """
        print(f"Error: {message}")

    def show_prompt(self, prompt: str) -> None:
        """Display a prompt for user input.

        Args:
            prompt: The prompt text (without trailing space)
        """
        print(prompt, end=" ", flush=True)
