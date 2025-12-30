"""Main entry point for the todo application.

This module provides the main() function that bootstraps
the application by initializing all components.

References:
- T027: Create main.py entry point
- T028: Wire up TaskStorage, TaskService, Display, and MenuController
"""

from .task_storage import TaskStorage
from .task_service import TaskService
from .display import Display
from .menu import MenuController


def main() -> None:
    """Application entry point.

    Initializes all components and starts the menu loop.
    """
    storage = TaskStorage()
    service = TaskService(storage)
    display = Display()
    menu = MenuController(service, display)
    menu.run()


if __name__ == "__main__":
    main()
