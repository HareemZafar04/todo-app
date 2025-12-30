# Phase I: Core Todo App Specification

**Feature**: Core Todo Application (Console)
**Phase**: I - Python Console Application
**Version**: 1.0.0
**Date**: 2025-12-30

## 1. Overview

### 1.1 Purpose
This specification defines Phase I of the "Evolution of Todo" project: a single-user, in-memory Python console application for task management.

### 1.2 Scope
Phase I delivers a fully functional command-line todo application with basic CRUD operations. Data exists only during runtime—no persistence, database, or external storage.

### 1.3 Out of Scope
- Any database (SQLite, PostgreSQL, etc.)
- File storage (JSON, CSV, or any file-based persistence)
- User authentication or multiple users
- Web APIs or HTTP concepts
- AI, chatbot, or LLM integration
- Cloud services or deployment
- Export/import functionality
- Categories, tags, or filtering
- Sorting or search functionality
- Undo/redo operations
-due dates or reminders

---

## 2. User Stories

### 2.1 Add Task
**As a** user,
**I want to** add new tasks to my todo list,
**So that** I can track things I need to do.

**Acceptance Criteria:**
- Given I am using the application
- When I choose to add a task
- And I enter a task title
- Then the task is added to my list
- And I receive confirmation of the addition
- And the task is assigned a unique ID

**Scenario: Adding a task with title only**
```
> Select action: 1. Add Task
> Enter task title: Buy groceries
Task added successfully! (ID: 1)
```

**Scenario: Adding a task with title and description**
```
> Select action: 1. Add Task
> Enter task title: Buy groceries
> Enter description (optional): Milk, eggs, bread
Task added successfully! (ID: 1)
```

### 2.2 View Task List
**As a** user,
**I want to** see all my tasks,
**So that** I can review what I need to do.

**Acceptance Criteria:**
- Given I have tasks in my list
- When I choose to view the task list
- Then I see all tasks displayed
- Each task shows: ID, title, description (if any), completion status
- Tasks are displayed in order of creation (oldest first)

**Scenario: Viewing tasks when list is empty**
```
> Select action: 2. View Tasks
No tasks found. Add a task to get started!
```

**Scenario: Viewing tasks with items**
```
> Select action: 2. View Tasks
ID | Title          | Status
----------------------------
1  | Buy groceries  | [ ]
2  | Call mom       | [x]
```

### 2.3 Update Task
**As a** user,
**I want to** update existing tasks,
**So that** I can correct or improve task details.

**Acceptance Criteria:**
- Given I have tasks in my list
- When I choose to update a task
- And I provide a valid task ID
- Then I can modify the title and/or description
- Changes are saved immediately

**Scenario: Updating task title**
```
> Select action: 3. Update Task
> Enter task ID: 1
> Enter new title (press Enter to keep 'Buy groceries'): Buy groceries and cleaning supplies
Task updated successfully!
```

### 2.4 Delete Task
**As a** a user,
**I want to** remove tasks from my list,
**So that** I can keep only relevant tasks.

**Acceptance Criteria:**
- Given I have tasks in my list
- When I choose to delete a task
- And I provide a valid task ID
- Then the task is permanently removed
- Task IDs of remaining tasks do not change

**Scenario: Deleting a task**
```
> Select action: 4. Delete Task
> Enter task ID: 1
Task deleted successfully!
```

### 2.5 Mark Task Complete / Incomplete
**As a** user,
**I want to** toggle task completion status,
**So that** I can track what I've done and what remains.

**Acceptance Criteria:**
- Given I have tasks in my list
- When I choose to mark a task complete
- And I provide a valid task ID
- Then the task's status changes to complete
- When I choose to mark a task incomplete
- Then the task's status changes to incomplete

**Scenario: Marking task complete**
```
> Select action: 5. Mark Complete
> Enter task ID: 1
Task marked as complete!
```

**Scenario: Marking task incomplete**
```
> Select action: 6. Mark Incomplete
> Enter task ID: 1
Task marked as incomplete!
```

---

## 3. Task Data Model

### 3.1 Task Class Definition

```python
from dataclasses import dataclass
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

### 3.2 Field Specifications

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `id` | int | Yes | Auto-generated | Unique positive integer, 1-based |
| `title` | str | Yes | N/A | 1-200 characters, non-empty |
| `description` | str | No | None | 0-1000 characters, optional |
| `completed` | bool | No | False | True/False only |
| `created_at` | datetime | Yes | Auto-generated | Immutable after creation |

### 3.3 ID Generation Strategy
- Task IDs are positive integers starting at 1
- IDs increment by 1 for each new task
- IDs never change (even after deletion)
- Deleted task IDs are not reused

### 3.4 In-Memory Storage
```python
# Global task storage (exists only during runtime)
tasks: list[Task] = []
next_task_id: int = 1
```

---

## 4. CLI Interaction Flow

### 4.1 Main Menu
The application displays a menu with options:

```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete
6. Mark Incomplete
7. Exit

Select an option (1-7):
```

### 4.2 Add Task Flow
```
1. User selects "1. Add Task"
2. Prompt: "Enter task title: "
3. User inputs title
   - If empty: Show error, return to menu
4. Prompt: "Enter description (optional): "
5. User inputs description (or presses Enter to skip)
6. Create task with auto-generated ID
7. Display confirmation: "Task added successfully! (ID: {id})"
8. Return to main menu
```

### 4.3 View Tasks Flow
```
1. User selects "2. View Tasks"
2. Check if tasks list is empty
   - If empty: Display "No tasks found..."
   - If not empty: Display formatted table
3. Return to main menu
```

### 4.4 Update Task Flow
```
1. User selects "3. Update Task"
2. Prompt: "Enter task ID: "
3. Validate task ID exists
   - If invalid: Show error, return to menu
4. Prompt: "Enter new title (press Enter to keep '{current}'): "
5. User inputs new title (or presses Enter to keep current)
6. Prompt: "Enter new description (press Enter to keep '{current}'): "
7. User inputs new description (or presses Enter to keep current)
8. Update task in memory
9. Display confirmation: "Task updated successfully!"
10. Return to main menu
```

### 4.5 Delete Task Flow
```
1. User selects "4. Delete Task"
2. Prompt: "Enter task ID: "
3. Validate task ID exists
   - If invalid: Show error, return to menu
4. Remove task from list
5. Display confirmation: "Task deleted successfully!"
6. Return to main menu
```

### 4.6 Mark Complete Flow
```
1. User selects "5. Mark Complete"
2. Prompt: "Enter task ID: "
3. Validate task ID exists
   - If invalid: Show error, return to menu
4. Set task.completed = True
5. Display confirmation: "Task marked as complete!"
6. Return to main menu
```

### 4.7 Mark Incomplete Flow
```
1. User selects "6. Mark Incomplete"
2. Prompt: "Enter task ID: "
3. Validate task ID exists
   - If invalid: Show error, return to menu
4. Set task.completed = False
5. Display confirmation: "Task marked as incomplete!"
6. Return to main menu
```

### 4.8 Exit Flow
```
1. User selects "7. Exit"
2. Display: "Goodbye!"
3. Application terminates
```

---

## 5. Acceptance Criteria Summary

### 5.1 Add Task
- [ ] Task is created with auto-incremented ID
- [ ] Title is required (1-200 characters)
- [ ] Description is optional
- [ ] Completed status defaults to False
- [ ] Confirmation message shows new task ID
- [ ] Empty title shows error message

### 5.2 View Tasks
- [ ] Empty list shows informative message
- [ ] Non-empty list displays in table format
- [ ] Each task shows ID, title, completion status
- [ ] Description shown if present
- [ ] Tasks ordered by creation time

### 5.3 Update Task
- [ ] Valid ID required
- [ ] Title can be kept or changed
- [ ] Description can be kept or changed
- [ ] Changes persist in memory
- [ ] Invalid ID shows error

### 5.4 Delete Task
- [ ] Valid ID required
- [ ] Task removed from list
- [ ] Confirmation displayed
- [ ] Invalid ID shows error
- [ ] Other task IDs unchanged

### 5.5 Toggle Completion
- [ ] Valid ID required
- [ ] Complete sets status to True
- [ ] Incomplete sets status to False
- [ ] Changes visible in task list
- [ ] Invalid ID shows error

### 5.6 General
- [ ] Application runs without errors
- [ ] Invalid menu choice shows error and reprompts
- [ ] Application can be exited cleanly
- [ ] No external dependencies required

---

## 6. Error Handling

### 6.1 Invalid Menu Choice
**Condition:** User enters non-numeric or out-of-range value
```
Select an option (1-7): 9
Invalid option. Please enter a number between 1 and 7.
```

### 6.2 Invalid Task ID (Update/Delete/Complete/Incomplete)
**Condition:** User enters ID that doesn't exist
```
Enter task ID: 999
Error: Task with ID 999 not found.
```

### 6.3 Empty Task List (View)
**Condition:** User views tasks when none exist
```
No tasks found. Add a task to get started!
```

### 6.4 Empty Title (Add Task)
**Condition:** User submits empty title
```
Enter task title:
Error: Title cannot be empty. Please enter a task title.
```

### 6.5 Non-numeric Input for Task ID
**Condition:** User enters non-numeric ID
```
Enter task ID: abc
Error: Please enter a valid number.
```

---

## 7. Constraints Verification

### 7.1 Phase I Constraints Checklist
| Constraint | Status | Notes |
|------------|--------|-------|
| No databases | ✅ | In-memory only |
| No file storage | ✅ | No JSON/CSV files |
| No authentication | ✅ | Single user |
| No APIs/web concepts | ✅ | CLI only |
| No advanced features | ✅ | Basic CRUD only |
| No AI/chatbot | ✅ | Console UI |
| No cloud concepts | ✅ | Local runtime |
| No future phase references | ✅ | Self-contained |

### 7.2 Compliance with Global Constitution
- ✅ SDD lifecycle followed: Constitution → Specify → Plan → Tasks → Implement
- ✅ Phase isolation maintained (no Phase II+ concepts)
- ✅ Specification-first approach
- ✅ Explicit ambiguity resolution documented

---

## 8. Definition of Done

The Phase I specification is complete when:
- [ ] All user stories written and approved
- [ ] Data model fully defined
- [ ] CLI interaction flows documented
- [ ] Acceptance criteria defined for each feature
- [ ] Error handling scenarios documented
- [ ] Constraints verified
- [ ] Plan phase can begin

---

**Spec Status**: Draft | **Author**: Claude Sonnet 4.5 | **Phase**: I
