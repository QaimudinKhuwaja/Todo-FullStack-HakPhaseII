description: "Frontend UI Implementation Tasks for Feature 007-frontend-ui-spec"
---

# Tasks: Frontend UI for Todo App

**Input**: Design documents from `/specs/007-frontend-ui-spec/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Paths must follow the monorepo structure: `backend/` and `frontend/`
- Paths shown below assume this structure.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Configure `NEXT_PUBLIC_API_BASE_URL` environment variable in `frontend/.env.local` or `frontend/.env.development.local`.
- [ ] T002 Initialize Tailwind CSS in `frontend` project (`frontend/tailwind.config.ts`, `frontend/src/app/globals.css`).
- [ ] T003 Create base `src/` directory and move `app/` into it (`frontend/src/`).
- [ ] T004 [P] Create `frontend/src/types/auth.ts` for authentication related types.
- [ ] T005 [P] Create `frontend/src/types/tasks.ts` for task related types.
- [ ] T006 [P] Create `frontend/src/lib/utils.ts` for general utility functions.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Implement base API client in `frontend/src/lib/api/client.ts`. (FR-026)
- [ ] T008 Create API endpoint definitions in `frontend/src/lib/api/endpoints.ts` for Auth and System endpoints. (FR-003, FR-004, FR-015)
- [ ] T009 Implement `middleware.ts` in project root for initial route protection and 401 redirection. (`frontend/middleware.ts`) (FR-014, FR-016)
- [ ] T010 Implement token handling functions for secure cookie storage in `frontend/src/lib/auth/token.ts`. (FR-005)
- [ ] T011 Create `AuthContext` or `useAuth` hook in `frontend/src/hooks/useAuth.ts` for global authentication state.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Login (Priority: P1) 🎯 MVP

**Goal**: A new user can register for an account, then log in using their credentials. An existing user can log in.

**Independent Test**: Can be tested by navigating to `/register`, creating an account, then navigating to `/login` and logging in successfully. Should redirect to `/dashboard`.

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create `AuthForm` component in `frontend/src/components/auth/AuthForm.tsx`.
- [ ] T013 [US1] Create registration page in `frontend/src/app/(auth)/register/page.tsx` using `AuthForm` and integrate with `POST /users/` endpoint. (FR-001, FR-003)
- [ ] T014 [US1] Create login page in `frontend/src/app/(auth)/login/page.tsx` using `AuthForm` and integrate with `POST /login` endpoint. (FR-002, FR-004)
- [ ] T015 [US1] Implement redirection to `/dashboard` on successful login/registration.
- [ ] T016 [US1] Display error messages for invalid login/registration credentials in `AuthForm`. (FR-018)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management (Priority: P1)

**Goal**: An authenticated user can view their list of tasks, create new tasks, update existing tasks, and delete tasks.

**Independent Test**: Can be tested by logging in, then creating, updating, and deleting tasks from the dashboard and task detail pages.

### Implementation for User Story 2

- [ ] T017 [P] [US2] Add API endpoint definitions for Task CRUD operations in `frontend/src/lib/api/endpoints.ts` (`GET /tasks/`, `POST /tasks/`, `GET /tasks/{task_id}`, `PATCH /tasks/{task_id}`, `DELETE /tasks/{task_id}`). (FR-009, FR-010, FR-011, FR-012, FR-013)
- [ ] T018 [P] [US2] Create `TaskCard` component in `frontend/src/components/tasks/TaskCard.tsx`.
- [ ] T019 [P] [US2] Create `TaskList` component in `frontend/src/components/tasks/TaskList.tsx`.
- [ ] T020 [P] [US2] Create `TaskForm` component in `frontend/src/components/tasks/TaskForm.tsx`.
- [ ] T021 [P] [US2] Create `DeleteConfirmationModal` component in `frontend/src/components/tasks/DeleteConfirmationModal.tsx`.
- [ ] T022 [US2] Implement dashboard page (`frontend/src/app/dashboard/page.tsx`) to display tasks using `TaskList` and allow task creation using `TaskForm`. (FR-007)
- [ ] T023 [US2] Implement task detail and edit page (`frontend/src/app/tasks/[id]/page.tsx`) using `TaskForm` and `DeleteConfirmationModal`. (FR-008)
- [ ] T024 [US2] Integrate update and delete functionality from `TaskCard` to `frontend/src/app/tasks/[id]/page.tsx`.
- [ ] T025 [US2] Implement real-time UI update after task creation, update, or deletion. (SC-002)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Session Management and Protected Routes (Priority: P1)

**Goal**: The application handles authentication tokens, protects routes from unauthenticated access, and allows users to log out.

**Independent Test**: Can be tested by trying to access protected routes without logging in, verifying token usage in API calls, and logging out.

### Implementation for User Story 3

- [ ] T026 [P] [US3] Refine `frontend/middleware.ts` to ensure comprehensive protection for `/dashboard` and `/tasks` routes, and redirection to `/login` for unauthenticated access. (FR-014)
- [ ] T027 [P] [US3] Create `LogoutButton` component in `frontend/src/components/auth/LogoutButton.tsx`.
- [ ] T028 [P] [US3] Create `Navbar` component in `frontend/src/components/common/Navbar.tsx` and integrate `LogoutButton`.
- [ ] T029 [US3] Implement logout functionality in `Navbar` (calls `POST /logout` endpoint, clears token, redirects to `/login`). (FR-015)
- [ ] T030 [US3] Ensure Authorization header is correctly attached to all protected API requests by `frontend/src/lib/api/client.ts`. (FR-006)
- [ ] T031 [US3] Implement 401 (Unauthorized) API response handling in `frontend/src/lib/api/client.ts` to redirect to `/login`. (FR-016)
- [ ] T032 [US3] Implement `frontend/src/app/page.tsx` to handle initial redirection (to `/login` if unauthenticated, to `/dashboard` if authenticated).

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T033 [P] Create `LoadingSpinner` component in `frontend/src/components/common/LoadingSpinner.tsx`.
- [ ] T034 [P] Create `ErrorDisplay` component in `frontend/src/components/common/ErrorDisplay.tsx`.
- [ ] T035 Integrate `LoadingSpinner` and `ErrorDisplay` into all relevant components and pages for API requests. (FR-018, FR-019)
- [ ] T036 Implement client-side form validations for `AuthForm` and `TaskForm`. (FR-017)
- [ ] T037 Ensure visual consistency and responsiveness using Tailwind CSS. (FR-020, FR-021, FR-022)
- [ ] T038 Implement visual distinction for completed tasks in `TaskCard` and `TaskList`. (FR-023)
- [ ] T039 Configure Next.js security headers in `frontend/next.config.js`.

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

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

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
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
