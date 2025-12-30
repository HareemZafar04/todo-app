"""Task data model for the todo application.

This module defines the Task dataclass used to represent
individual todo items in the in-memory task list.

References:
- T004: Create Task data model in src/task.py
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique positive integer identifier (auto-assigned)
        title: Task title (1-200 characters, required)
        description: Optional task description (0-1000 characters)
        completed: Whether the task is complete (default False)
        created_at: Timestamp when task was created (immutable)
    """
    title: str
    description: Optional[str] = None
    completed: bool = False
    id: int = 0
    created_at: datetime = field(default_factory=datetime.now)
