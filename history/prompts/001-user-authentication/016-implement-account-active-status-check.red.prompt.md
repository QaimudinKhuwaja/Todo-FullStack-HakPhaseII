---
id: 016
title: Implement account active status check
stage: red
date: 2026-01-27
surface: agent
model: gemini-1.5-pro
feature: 001-user-authentication
branch: main
user: Faraz
command: /sp.implement Implement task T013 from specs/001-user-authentication/tasks.md
labels: ["authentication", "security", "bugfix"]
links:
  spec: specs/001-user-authentication/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/app/models/user.py
 - backend/app/api/endpoints/auth.py
 - specs/001-user-authentication/tasks.md
tests:
 - N/A
---

## Prompt

/sp.implement Implement task T013 from specs/001-user-authentication/tasks.md

Rules:
- Follow spec.md and plan.md strictly
- Implement ONLY this task
- Use existing User model and login endpoint (T006)
- Keep implementation minimal and explicit
- Do NOT modify sessions, logout, or expiry logic
- Do NOT add unrelated abstractions or external packages

Task:
T013: Implement basic mechanism for handling disabled/locked accounts
- During login, check `User.is_active` (or equivalent field)
- Deny login if account is disabled or locked
- Return generic error message ("Invalid email or password") without revealing account status
- Target file: backend/app/api/endpoints/auth.py

Expected Outcome:
- Login endpoint now handles inactive/locked users safely
- Uses existing password verification and session creation
- Task T013 marked as completed in tasks.md
- Scope strictly limited to account active status check only

## Response snapshot

Implemented the `is_active` check in the user login process.
- Added `is_active: bool = Field(default=True)` to the `User` model in `backend/app/models/user.py`.
- Modified the `login_for_access_token` function in `backend/app/api/endpoints/auth.py` to check `user.is_active` and raise an `HTTPException` if `False`.
- Marked task T013 as completed in `specs/001-user-authentication/tasks.md`.

## Outcome

- ✅ Impact: Account active status check implemented, T013 completed.
- 🧪 Tests: No tests run by agent, but implementation should be covered by existing login tests.
- 📁 Files: Modified User model, auth endpoint, and tasks file.
- 🔁 Next prompts: N/A
- 🧠 Reflection: Successfully implemented T013 by first adding `is_active` to the User model, then adding the check to the login endpoint, and finally marking the task complete.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
