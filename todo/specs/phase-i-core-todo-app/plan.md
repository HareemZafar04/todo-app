# Phase I: Technical Plan

**Feature**: Core Todo Application (Console)
**Phase**: I - Python Console Application
**Based On**: `specs/phase-i-core-todo-app/spec.md`
**Version**: 1.0.0
**Date**: 2025-12-30

## 1. Application Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│              Todo Application (Console)              │
├─────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────┐  │
│  │              Application Entry Point          │  │
│  │              (main.py / todo.py)              │  │
│  └───────────────────────────────────────────────┘  │
│                          │                           │
│                          ▼                           │
│  ┌───────────────────────────────────────────────┐  │
│  │              Menu Controller                   │  │
│  │         (dispatcher, input handling)          │  │
│  └───────────────────────────────────────────────┘  │
│                          │                           │
│          ┌───────────────┼───────────────┐          │
│          ▼               ▼               ▼          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Task      │  │   Task      │  │   Task      │  │
│  │  Storage    │  │  Operations │  │  Display    │  │
│  │  (In-Memory)│  │   (Logic)   │  │  (Formatter)│  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────┘
```

### 1.2 Architecture Principles

- **Single Process**: Everything runs in one Python process
- **Synchronous Execution**: No async/await, simple blocking I/O
- **In-Memory State**: All data exists in Python objects only
- **Terminal I/O**: Standard input/output via `input()` and `print()`

---

## 2. Component Breakdown

### 2.1 Component Overview

| Component | File | Responsibility |
|-----------|------|----------------|
| Application Entry | `src/main.py` | Startup, main loop, cleanup |
| Menu Controller | `src/menu.py` | Display menu, route input |
| Task Operations | `src/task_service.py` | CRUD operations, business logic |
| Task Storage | `src/task_storage.py` | In-memory list management |
| Task Model | `src/task.py` | Task dataclass definition |
| Display Formatter | `src/display.py` | Table formatting, messages |

### 2.2 Component Details

#### 2.2.1 Task Model (`src/task.py`)
```
Responsibility: Define Task data structure
Dependencies: dataclasses, typing
Exports: Task class
```

**Implementation:**
```python
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class Task:
    """Represents a single todo task."""
    title: str
    description: Optional[str] = None
    completed: bool = False
    id: int = 0
    created_at: datetime = field(default_factory=datetime.now)
```

#### 2.2.2 Task Storage (`src/task_storage.py`)
```
Responsibility: Manage in-memory task list
Dependencies: Task model
Exports: TaskStorage class
```

**Methods:**
- `add_task(task: Task) -> Task` - Add task, assign ID
- `get_task(id: int) -> Optional[Task]` - Retrieve by ID
- `get_all_tasks() -> list[Task]` - Return all tasks
- `update_task(id: int, **kwargs) -> bool` - Update fields
- `delete_task(id: int) -> bool` - Remove task
- `mark_complete(id: int) -> bool` - Set completed=True
- `mark_incomplete(id: int) -> bool` - Set completed=False

**Internal State:**
```python
class TaskStorage:
    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1
```

#### 2.2.3 Task Operations (`src/task_service.py`)
```
Responsibility: Business logic orchestration
Dependencies: TaskStorage
Exports: TaskService class
```

**Methods:**
- `create_task(title: str, description: Optional[str] = None) -> Task`
- `list_tasks() -> list[Task]`
- `update_task(id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool`
- `delete_task(id: int) -> bool`
- `complete_task(id: int) -> bool`
- `incomplete_task(id: int) -> bool`

**Validation Logic:**
- Title length: 1-200 characters
- Description length: 0-1000 characters
- ID existence verification

#### 2.2.4 Display Formatter (`src/display.py`)
```
Responsibility: Format output for terminal
Dependencies: Task model
Exports: Display class
```

**Methods:**
- `show_menu()` - Print main menu
- `show_tasks(tasks: list[Task])` - Format and print task table
- `show_message(message: str)` - Print info/warning/error
- `show_confirmation(action: str)` - Print success message
- `format_task_table(tasks: list[Task]) -> str` - Generate table string
- `format_task_row(task: Task) -> str` - Format single row

**Table Format:**
```
ID | Title          | Status
----------------------------
1  | Buy groceries  | [ ]
2  | Call mom       | [x]
```

#### 2.2.5 Menu Controller (`src/menu.py`)
```
Responsibility: Handle user input, dispatch actions
Dependencies: TaskService, Display
Exports: MenuController class
```

**Methods:**
- `run()` - Start the menu loop
- `handle_input()` - Read and parse user input
- `dispatch(option: int)` - Route to appropriate handler
- `_handle_add()` - Add task flow
- `_handle_view()` - View tasks flow
- `_handle_update()` - Update task flow
- `_handle_delete()` - Delete task flow
- `_handle_complete()` - Mark complete flow
- `_handle_incomplete()` - Mark incomplete flow
- `_handle_exit()` - Clean exit

**Input Handling:**
- Validate numeric input
- Range validation (1-7)
- Reprompt on invalid input

#### 2.2.6 Application Entry Point (`src/main.py`)
```
Responsibility: Bootstrap application
Dependencies: MenuController
Exports: main() function
```

**Implementation:**
```python
from menu import MenuController
from task_service import TaskService
from task_storage import TaskStorage

def main():
    """Application entry point."""
    storage = TaskStorage()
    service = TaskService(storage)
    menu = MenuController(service)
    menu.run()

if __name__ == "__main__":
    main()
```

---

## 3. Data Structures

### 3.1 In-Memory Task Storage

```python
# Global module-level storage (per spec)
class TaskStorage:
    _tasks: list[Task] = []
    _next_id: int = 1
```

**Data Structure Characteristics:**
- **Type**: Python list (`list[Task]`)
- **Order**: Maintained by insertion order
- **Access**: Sequential scan for ID lookup (O(n))
- **Persistence**: None (cleared on exit)

### 3.2 Task ID Generation

```python
class TaskStorage:
    def _generate_id(self) -> int:
        """Generate next available ID."""
        current = self._next_id
        self._next_id += 1
        return current
```

**ID Strategy:**
- Starting value: 1
- Increment: 1 per new task
- No reuse after deletion
- Immutable for existing tasks

### 3.3 Memory Usage

| Scenario | Estimated Memory |
|----------|------------------|
| Empty list | ~56 bytes (list overhead) |
| 100 tasks | ~5-10 KB |
| 1000 tasks | ~50-100 KB |

---

## 4. Control Flow

### 4.1 Application Startup

```
main() called
    │
    ▼
Create TaskStorage instance
    │
    ▼
Create TaskService with storage
    │
    ▼
Create MenuController with service
    │
    ▼
Call menu.run()
```

### 4.2 Menu Loop

```
menu.run() started
    │
    ┌─────────────────────────────┐
    │     WHILE True              │
    │  ┌───────────────────────┐  │
    │  │ display.show_menu()   │  │
    │  └───────────────────────┘  │
    │            │                 │
    │            ▼                 │
    │  ┌───────────────────────┐  │
    │  │ input() → user_input  │  │
    │  └───────────────────────┘  │
    │            │                 │
    │            ▼                 │
    │  ┌───────────────────────┐  │
    │  │ Validate numeric?     │──┼── No ──▶ Show error, continue
    │  └───────────────────────┘  │
    │            │ Yes             │
    │            ▼                 │
    │  ┌───────────────────────┐  │
    │  │ Valid range (1-7)?    │──┼── No ──▶ Show error, continue
    │  └───────────────────────┘  │
    │            │ Yes             │
    │            ▼                 │
    │  ┌───────────────────────┐  │
    │  │ dispatch(option)      │  │
    │  └───────────────────────┘  │
    │            │                 │
    │     ┌──────┴──────┐          │
    │     ▼             ▼          │
    │  Option 7    Other option    │
    │  (Exit)       (Process)      │
    │     │             │          │
    │     ▼             │          │
    │  Break loop       │          │
    │     │             │          │
    └─────┴─────────────┘          │
            │                      │
            ▼                      │
    display.show_message("Goodbye!")
    │
    ▼
Function returns, process exits
```

### 4.3 User Input Processing

```
input() reads line
    │
    ▼
strip() whitespace
    │
    ▼
isnumeric() check
    │
    ├─ False → Error: "Please enter a valid number"
    │
    ▼
int() conversion
    │
    ▼
1 <= option <= 7 check
    │
    ├─ False → Error: "Invalid option"
    │
    ▼
dispatch(option)
```

### 4.4 Feature Flows

#### Add Task Flow
```
_handle_add()
    │
    ▼
prompt "Enter task title: "
    │
    ▼
input() → validate not empty
    │
    ├─ empty → Error → return to menu
    │
    ▼
prompt "Enter description (optional): "
    │
    ▼
input() → if empty, store None
    │
    ▼
service.create_task(title, description)
    │
    ▼
display.show_confirmation(f"Task added successfully! (ID: {id})")
```

#### View Tasks Flow
```
_handle_view()
    │
    ▼
service.list_tasks()
    │
    ▼
if not tasks:
    │
    ▼
display.show_message("No tasks found...")
    │
    ▼
else:
    │
    ▼
display.show_tasks(tasks)
```

#### Update Task Flow
```
_handle_update()
    │
    ▼
prompt "Enter task ID: "
    │
    ▼
validate ID exists in storage
    │
    ├─ not found → Error → return to menu
    │
    ▼
prompt "Enter new title (press Enter to keep '{current}'): "
    │
    ▼
input() → if empty, keep current
    │
    ▼
prompt "Enter new description (press Enter to keep '{current}'): "
    │
    ▼
input() → if empty, keep current
    │
    ▼
service.update_task(id, title, description)
    │
    ▼
display.show_confirmation("Task updated successfully!")
```

#### Delete Task Flow
```
_handle_delete()
    │
    ▼
prompt "Enter task ID: "
    │
    ▼
validate ID exists
    │
    ├─ not found → Error → return to menu
    │
    ▼
service.delete_task(id)
    │
    ▼
display.show_confirmation("Task deleted successfully!")
```

#### Mark Complete Flow
```
_handle_complete()
    │
    ▼
prompt "Enter task ID: "
    │
    ▼
validate ID exists
    │
    ├─ not found → Error → return to menu
    │
    ▼
service.complete_task(id)
    │
    ▼
display.show_confirmation("Task marked as complete!")
```

### 4.5 Graceful Exit

```
_handle_exit()
    │
    ▼
display.show_message("Goodbye!")
    │
    ▼
return from handler
    │
    ▼
menu loop breaks
    │
    ▼
run() returns
    │
    ▼
main() returns
    │
    ▼
Python process exits
```

---

## 5. File Structure

### 5.1 Project Directory Layout

```
todo/
├── src/
│   ├── __init__.py          # Package marker
│   ├── task.py              # Task dataclass
│   ├── task_storage.py      # In-memory storage class
│   ├── task_service.py      # Business logic
│   ├── display.py           # Output formatting
│   ├── menu.py              # Menu controller
│   └── main.py              # Application entry point
├── tests/
│   ├── __init__.py
│   ├── test_task.py
│   ├── test_storage.py
│   ├── test_service.py
│   └── test_menu.py
├── specs/
│   └── phase-i-core-todo-app/
│       ├── spec.md          # Requirements (approved)
│       └── plan.md          # This document
├── history/
│   └── prompts/
│       └── phase-i-core-todo-app/
│           └── *.prompt.md  # PHR records
├── requirements.txt         # Dependencies
└── README.md                # Documentation
```

### 5.2 Source File Responsibilities

| File | Lines (est.) | Responsibility |
|------|-------------|----------------|
| `src/task.py` | 15-20 | Data class definition |
| `src/task_storage.py` | 40-50 | List management, ID generation |
| `src/task_service.py` | 60-80 | Validation, business rules |
| `src/display.py` | 50-70 | String formatting, output |
| `src/menu.py` | 80-120 | Input handling, dispatch |
| `src/main.py` | 10-15 | Bootstrap |
| **Total** | **~255-335** | |

---

## 6. Dependencies

### 6.1 Python Version
- **Minimum**: Python 3.10 (for dataclass features)
- **Recommended**: Python 3.11+ (performance)

### 6.2 Standard Library Only
| Module | Usage |
|--------|-------|
| `dataclasses` | Task definition |
| `typing` | Type hints |
| `datetime` | Timestamp tracking |

### 6.3 No External Dependencies
- No `pip install` required
- No third-party packages
- Runs with standard Python installation

---

## 7. Error Taxonomy

### 7.1 Error Types

| Error | Input | Message | Handling |
|-------|-------|---------|----------|
| Invalid menu choice | "9" or "abc" | "Invalid option..." | Reprompt |
| Non-numeric ID | "abc" | "Please enter a valid number" | Reprompt |
| Task not found | ID 999 | "Task with ID 999 not found" | Reprompt |
| Empty title | "" | "Title cannot be empty" | Reprompt |
| Empty task list | View | "No tasks found..." | Info message |

### 7.2 Error Handling Strategy

```python
def safe_input(prompt: str) -> str:
    """Get input with error handling."""
    while True:
        try:
            return input(prompt)
        except (EOFError, OSError):
            print("Error reading input. Please try again.")
```

---

## 8. Key Decisions

### 8.1 Decisions Made

| Decision | Rationale |
|----------|-----------|
| Dataclass for Task | Immutable-ish, clear fields, auto `__repr__` |
| Service/Storage separation | Testability, single responsibility |
| Menu controller pattern | Clean dispatch, easy to extend |
| String-based table output | No dependencies, terminal-compatible |
| Sequential ID | Simple, predictable, matches spec |

### 8.2 Alternative Considered

| Alternative | Rejected Because |
|-------------|------------------|
| Pydantic for validation | External dependency |
| Rich library for tables | External dependency |
| Class-based menus | Over-engineering for 7 options |
| UUID for IDs | Spec requires auto-increment integers |

---

## 9. Non-Functional Requirements

### 9.1 Performance
- **Startup**: < 0.1 seconds
- **Memory**: < 10 MB for 1000 tasks
- **Response**: Immediate (no I/O wait)

### 9.2 Reliability
- No external dependencies to fail
- Graceful handling of Ctrl+C
- Input validation on all paths

### 9.3 Portability
- Works on Windows, macOS, Linux
- Works in any terminal
- No platform-specific code

---

## 10. Definition of Done (Plan)

- [ ] Architecture approved
- [ ] Component breakdown reviewed
- [ ] Control flow validated
- [ ] File structure confirmed
- [ ] Ready for `/sp.tasks`

---

**Plan Status**: Draft | **Author**: Claude Sonnet 4.5 | **Phase**: I
**Based On**: `specs/phase-i-core-todo-app/spec.md` (v1.0.0)
