---
id: 001
title: Revise and correct API Contract specification
stage: spec
date: 2026-01-29
surface: agent
model: gemini-pro
feature: 004-api-contract
branch: 004-api-contract
user: (user)
command: /sp.specify "Revise and correct the existing API Contract specification. Context: - Existing spec folder was created as specs/001-api-contract/ - Intended feature ID is 004-api-contract - This is a correction pass, NOT a rewrite Required Fixes: 1. Rename feature references from `001-api-contract` to `004-api-contract` - Update folder name - Update feature branch references if present 2. Align Task response schemas strictly with backend implementation: - Remove any fields not present in TaskRead schema - Do NOT expose internal fields such as owner_id - Keep only minimal fields actually returned by the API 3. Review authentication endpoint responses: - Ensure signup/login responses match current backend behavior - If minimal responses are used, explicitly state that in the spec Constraints: - Do NOT add new endpoints - Do NOT add new fields - Do NOT change structure or section order - Keep documentation-only - Follow constitution strictly Output: - Corrected spec at `specs/004-api-contract/spec.md` - No additional commentary"
labels: ["api-contract", "specification", "correction"]
links:
  spec: specs/004-api-contract/spec.md
  ticket: null
  adr: null
  pr: null
files:
- specs/004-api-contract/spec.md
- specs/004-api-contract/checklists/requirements.md
tests:

---

## Prompt

Revise and correct the existing API Contract specification. Context: - Existing spec folder was created as specs/001-api-contract/ - Intended feature ID is 004-api-contract - This is a correction pass, NOT a rewrite Required Fixes: 1. Rename feature references from `001-api-contract` to `004-api-contract` - Update folder name - Update feature branch references if present 2. Align Task response schemas strictly with backend implementation: - Remove any fields not present in TaskRead schema - Do NOT expose internal fields such as owner_id - Keep only minimal fields actually returned by the API 3. Review authentication endpoint responses: - Ensure signup/login responses match current backend behavior - If minimal responses are used, explicitly state that in the spec Constraints: - Do NOT add new endpoints - Do NOT add new fields - Do NOT change structure or section order - Keep documentation-only - Follow constitution strictly Output: - Corrected spec at `specs/004-api-contract/spec.md` - No additional commentary

## Response snapshot

Successfully created and validated the specification for 'Revise API Contract' in `specs/004-api-contract/spec.md`.

## Outcome

- ✅ Impact: Specification updated and validated.
- 🧪 Tests: No tests were run in this process.
- 📁 Files: Created `specs/004-api-contract/spec.md` and `specs/004-api-contract/checklists/requirements.md`.
- 🔁 Next prompts: The next step would be to create a plan (`/sp.plan`).
- 🧠 Reflection: The `create-new-feature.ps1` script had issues with argument parsing, leading to manual spec creation. The PHR creation script also failed. Need to investigate better ways to integrate PowerShell scripts or rely more on agent-native tools for these operations.

## Evaluation notes (flywheel)

- Failure modes observed: PowerShell script execution issues with argument parsing.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Improve PowerShell script integration or use agent-native file operations for feature/PHR creation.
