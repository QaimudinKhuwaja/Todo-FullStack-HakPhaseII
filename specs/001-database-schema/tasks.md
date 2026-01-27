---

description: "Task list for 001-database-schema feature implementation"
---

# Tasks: 001-database-schema

**Input**: Design documents from `/specs/001-database-schema/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Paths must follow the monorepo structure: `backend/`
- Paths shown below assume this structure.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and setting up the Python environment for backend models.

- [ ] T001 Ensure `SQLModel` and `psycopg2-binary` are listed in `backend/requirements.txt`.
- [ ] T002 Create initial structure for database models in `backend/app/models/__init__.py` and other model files.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database connection and session management.

- [ ] T003 Configure the database engine for PostgreSQL using `SQLModel` in `backend/app/core/db.py`.
- [ ] T004 Implement session management and utility functions for database interactions in `backend/app/core/db.py`.

---

## Phase 3: User Story 1 - User Model Schema (Priority: P1)

**Goal**: Define the `User` model in `SQLModel` with `id`, `email`, `created_at` and enforce uniqueness for email.

**Independent Test**: Verify the `User` model can be created, saved, and retrieved, and that email uniqueness is enforced at the schema level.

### Implementation for User Story 1

- [ ] T005 [P] [US1] Create `User` model definition with `id`, `email`, `created_at` fields in `backend/app/models/user.py`.
- [ ] T006 [US1] Add `email` uniqueness constraint to the `User` model in `backend/app/models/user.py`.

---

## Phase 4: User Story 2 - Todo Model Schema and Relationships (Priority: P1)

**Goal**: Define the `Todo` model and establish the one-to-many relationship with the `User` model.

**Independent Test**: Verify the `Todo` model can be created, saved, and retrieved, associated with a `User`, and that foreign key constraints are enforced.

### Implementation for User Story 2

- [ ] T007 [P] [US2] Create `Todo` model definition with `id`, `user_id`, `title`, `description`, `completed`, `created_at`, `updated_at` fields in `backend/app/models/todo.py`.
- [ ] T008 [US2] Define the one-to-many relationship between `User` and `Todo` models in `backend/app/models/user.py` and `backend/app/models/todo.py`.
- [ ] T009 [US2] Ensure foreign key constraint for `user_id` in the `Todo` model in `backend/app/models/todo.py`.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Schema-level testing and final checks.

- [ ] T010 [P] Implement schema-level tests for `User` model data integrity (e.g., email uniqueness) in `backend/tests/models/test_user.py`.
- [ ] T011 [P] Implement schema-level tests for `Todo` model data integrity and relationship with `User` (e.g., foreign key, cascade delete) in `backend/tests/models/test_todo.py`.
- [ ] T012 Verify all model definitions are correctly imported and accessible (e.g., via `backend/app/models/__init__.py`).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - User Model Schema)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1 - Todo Model Schema and Relationships)**: Can start after Foundational (Phase 2) - Depends on User Story 1 (User model must exist)

### Within Each User Story

- Models before services (N/A for this feature as no services are being built)
- Core model definition before relationships/constraints
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel.
- All Foundational tasks can be worked on.
- Once Foundational phase completes, tasks within User Stories marked [P] can run in parallel.
- Different user stories can be worked on in parallel by different team members (with careful management of inter-story dependencies).

---

## Parallel Example: User Story 1

```bash
# Launch all tasks for User Story 1 together (if tests requested):
Task: "Create User model definition with id, email, created_at fields in backend/app/models/user.py"
Task: "Add email uniqueness constraint to the User model in backend/app/models/user.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
