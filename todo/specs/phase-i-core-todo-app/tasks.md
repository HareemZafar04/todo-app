# Tasks: Phase I - Core Todo App

**Feature**: Core Todo Application (Console)
**Phase**: I - Python Console Application
**Input**: `specs/phase-i-core-todo-app/spec.md`, `specs/phase-i-core-todo-app/plan.md`
**Version**: 1.0.0
**Date**: 2025-12-30

**Tests**: None requested - proceeding directly to implementation

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure per plan (src/, tests/)
- [X] T002 Create requirements.txt with Python 3.10+ requirement (no external deps)
- [X] T003 Create src/__init__.py package marker

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Create Task data model in src/task.py (Task dataclass with id, title, description, completed, created_at)
- [X] T005 [P] Create TaskStorage class in src/task_storage.py (in-memory list, ID generation)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1) MVP

**Goal**: User can create new tasks with title and optional description

**Independent Test**: Run app, select option 1, enter title, see confirmation with ID

### Implementation for User Story 1

- [X] T006 [US1] Create task_service.py with create_task() method in src/task_service.py
- [X] T007 [US1] Create display.py with show_menu() and show_confirmation() in src/display.py
- [X] T008 [US1] Create menu.py with _handle_add() method in src/menu.py
- [X] T009 [US1] Add validation for empty title in task_service.py

**Checkpoint**: Add Task feature should be functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: User can see all tasks in a formatted table display

**Independent Test**: Run app with tasks added, select option 2, see table of tasks

### Implementation for User Story 2

- [X] T010 [US2] Add list_tasks() method to TaskStorage in src/task_storage.py
- [X] T011 [US2] Add list_tasks() method to TaskService in src/task_service.py
- [X] T012 [US2] Add show_tasks() and format_task_table() methods to display.py
- [X] T013 [US2] Add _handle_view() method to menu.py

**Checkpoint**: View Tasks feature should be functional and testable independently

---

## Phase 5: User Story 3 - Update Task (Priority: P2)

**Goal**: User can modify title and/or description of existing tasks

**Independent Test**: Run app, create task, select option 3, update title, verify change

### Implementation for User Story 3

- [X] T014 [US3] Add update_task() method to TaskStorage in src/task_storage.py
- [X] T015 [US3] Add update_task() method to TaskService in src/task_service.py
- [X] T016 [US3] Add _handle_update() method to menu.py

**Checkpoint**: Update Task feature should be functional and testable independently

---

## Phase 6: User Story 4 - Delete Task (Priority: P2)

**Goal**: User can remove tasks from the list by ID

**Independent Test**: Run app, create task, select option 4, enter ID, task removed

### Implementation for User Story 4

- [X] T017 [US4] Add delete_task() method to TaskStorage in src/task_storage.py
- [X] T018 [US4] Add delete_task() method to TaskService in src/task_service.py
- [X] T019 [US4] Add _handle_delete() method to menu.py

**Checkpoint**: Delete Task feature should be functional and testable independently

---

## Phase 7: User Story 5 - Mark Complete / Incomplete (Priority: P3)

**Goal**: User can toggle task completion status

**Independent Test**: Run app, create task, select option 5, verify [x] status, select option 6, verify [ ] status

### Implementation for User Story 5

- [X] T020 [US5] Add mark_complete() and mark_incomplete() methods to TaskStorage in src/task_storage.py
- [X] T021 [US5] Add complete_task() and incomplete_task() methods to TaskService in src/task_service.py
- [X] T022 [US5] Add _handle_complete() and _handle_incomplete() methods to menu.py

**Checkpoint**: Mark Complete/Incomplete feature should be functional and testable independently

---

## Phase 8: Error Handling (Cross-Cutting)

**Purpose**: Robust input validation and error messages across all features

- [X] T023 Add input validation in menu.py (numeric check, range check)
- [X] T024 Add task_not_found error handling in menu.py
- [X] T025 Add show_message() for empty list in display.py
- [X] T026 Add error messages for invalid inputs throughout

---

## Phase 9: Application Entry Point

**Purpose**: Bootstrap the application with proper initialization

- [X] T027 Create main.py entry point in src/main.py
- [X] T028 Wire up TaskStorage, TaskService, Display, and MenuController in main.py
- [X] T029 Add graceful exit handling in menu.py (_handle_exit)

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final integration and verification

- [X] T030 [P] Create tests/__init__.py package marker
- [X] T031 [P] Verify all acceptance criteria from spec.md
- [X] T032 Run manual validation against all CLI interaction flows

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|-----------|--------|
| Setup (1) | None | Foundational |
| Foundational (2) | Setup | All User Stories |
| US1 Add Task (3) | Foundational | US1 Complete |
| US2 View Tasks (4) | Foundational | US2 Complete |
| US3 Update Task (5) | Foundational | US3 Complete |
| US4 Delete Task (6) | Foundational | US4 Complete |
| US5 Toggle (7) | Foundational | US5 Complete |
| Error Handling (8) | All User Stories | Entry Point |
| Entry Point (9) | Foundational + Error Handling | Polish |
| Polish (10) | All Previous | Done |

### User Story Dependencies

All user stories (US1-US5) depend only on Foundational (Phase 2) completion.
- **User Story 1 (Add Task)**: No dependencies on other stories
- **User Story 2 (View Tasks)**: No dependencies on other stories
- **User Story 3 (Update Task)**: No dependencies on other stories
- **User Story 4 (Delete Task)**: No dependencies on other stories
- **User Story 5 (Toggle)**: No dependencies on other stories

### Within Each User Story

- Storage methods before Service methods
- Service methods before Menu handlers
- Display formatting before Menu usage

### Parallel Opportunities

- Phase 1 tasks can run in parallel
- Phase 2 tasks (T004, T005) can run in parallel (different files)
- User stories can proceed in parallel after Foundational
- Within each story: Display tasks can proceed in parallel with Storage additions

---

## Parallel Example: Foundational Phase

```bash
# T004 and T005 can run in parallel:
Task: "Create Task data model in src/task.py"
Task: "Create TaskStorage class in src/task_storage.py"
```

## Parallel Example: User Story 1

```bash
# T006, T007 can run in parallel:
Task: "Create task_service.py with create_task()"
Task: "Create display.py with show_menu()"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Add Task)
4. **STOP and VALIDATE**: Test Add Task independently
5. If MVP is sufficient, stop here

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently
3. Add User Story 2 → Test independently (US2 can use T010, T011, T012, T013)
4. Add User Story 3 → Test independently (US3 builds on T014, T015, T016)
5. Add User Story 4 → Test independently (US4 builds on T017, T018, T019)
6. Add User Story 5 → Test independently (US5 builds on T020, T021, T022)
7. Complete remaining phases

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

**Tasks Version**: 1.0.0 | **Total Tasks**: 32 | **Feature**: phase-i-core-todo-app
**Status**: ALL TASKS COMPLETED - Ready for Phase II
