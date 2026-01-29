# Feature Specification: Revise API Contract

**Feature Branch**: `004-api-contract`  
**Created**: 2026-01-29  
**Status**: Draft  
**Input**: User description: "Revise and correct the existing API Contract specification. Context: - Existing spec folder was created as specs/001-api-contract/ - Intended feature ID is 004-api-contract - This is a correction pass, NOT a rewrite Required Fixes: 1. Rename feature references from `001-api-contract` to `004-api-contract` - Update folder name - Update feature branch references if present 2. Align Task response schemas strictly with backend implementation: - Remove any fields not present in TaskRead schema - Do NOT expose internal fields such as owner_id - Keep only minimal fields actually returned by the API 3. Review authentication endpoint responses: - Ensure signup/login responses match current backend behavior - If minimal responses are used, explicitly state that in the spec Constraints: - Do NOT add new endpoints - Do NOT add new fields - Do NOT change structure or section order - Keep documentation-only - Follow constitution strictly Output: - Corrected spec at `specs/004-api-contract/spec.md` - No additional commentary"

## User Scenarios & Testing

### User Story 1 - Verify Task Schema Alignment (Priority: P1)

An API consumer retrieves a list of tasks or a single task and expects the response schema to precisely match the documented contract, which should strictly reflect the backend's `TaskRead` schema, excluding any internal or non-exposed fields like `owner_id`.

**Why this priority**: Ensuring the API contract accurately represents the actual data returned is critical for reliable client-side development and integration, preventing unexpected data structures and potential security concerns from exposing internal details.

**Independent Test**: Can be fully tested by making API requests to task endpoints (e.g., GET /tasks, GET /tasks/{id}) and verifying the structure and content of the JSON response against the updated specification.

**Acceptance Scenarios**:

1.  **Given** an authenticated API consumer, **When** they request all tasks, **Then** the response for each task MUST conform to the updated `Task` schema in the spec, containing only the explicitly allowed fields.
2.  **Given** an authenticated API consumer, **When** they request a single task by ID, **Then** the response for that task MUST conform to the updated `Task` schema in the spec, containing only the explicitly allowed fields.
3.  **Given** an authenticated API consumer, **When** they receive a task response, **Then** the `owner_id` field MUST NOT be present in the response.

### User Story 2 - Verify Auth Endpoint Responses (Priority: P1)

An API consumer performs user authentication operations (signup, login) and expects the API responses (both success and failure) to strictly match the documented contract, reflecting the current backend behavior, including explicit statements if minimal responses are intentionally provided.

**Why this priority**: Consistent and clearly documented authentication responses are fundamental for secure and robust client applications, enabling predictable handling of user sessions and error conditions.

**Independent Test**: Can be fully tested by making API requests to authentication endpoints (e.g., POST /signup, POST /login) with various valid and invalid credentials, and verifying the structure and content of the JSON responses against the updated specification.

**Acceptance Scenarios**:

1.  **Given** an unauthenticated API consumer, **When** they attempt to sign up with valid credentials, **Then** the response MUST accurately reflect the documented success response for signup, matching backend behavior.
2.  **Given** an unauthenticated API consumer, **When** they attempt to log in with valid credentials, **Then** the response MUST accurately reflect the documented success response for login (e.g., containing `access_token`, `token_type`), matching backend behavior.
3.  **Given** an unauthenticated API consumer, **When** they attempt to log in with invalid credentials, **Then** the response MUST accurately reflect the documented error response for failed login, matching backend behavior.
4.  **Given** that authentication responses are intentionally minimal, **When** reviewing the spec, **Then** the spec MUST explicitly state this design choice for the relevant authentication endpoints.

## Requirements

### Functional Requirements

-   **FR-001**: The API Contract specification MUST accurately reflect the `TaskRead` schema from the backend implementation, excluding internal fields such as `owner_id`.
-   **FR-002**: The API Contract specification MUST explicitly define the minimal set of fields returned for `Task` resources, aligning with the backend implementation.
-   **FR-003**: The API Contract specification MUST ensure that authentication endpoint responses (signup/login) precisely match the current backend behavior.
-   **FR-004**: If authentication endpoint responses are minimal, the API Contract specification MUST explicitly state this.
-   **FR-005**: The API Contract specification MUST NOT introduce new endpoints.
-   **FR-006**: The API Contract specification MUST NOT introduce new fields to existing schemas.
-   **FR-007**: The API Contract specification MUST maintain its existing structure and section order.

### Key Entities

-   **Task**: Represents a task entity, with attributes limited to those exposed by the API (e.g., `id`, `title`, `description`, `status`).
-   **User (Auth)**: Represents authentication-related entities, specifically for signup and login responses (e.g., `access_token`, `token_type` for successful login, or specific error messages for failures).

## Success Criteria

### Measurable Outcomes

-   **SC-001**: The `specs/004-api-contract/spec.md` file will be created and contain all corrections outlined in the prompt.
-   **SC-002**: All `Task` related schemas in `spec.md` will strictly align with the backend's `TaskRead` model, exposing only non-internal fields.
-   **SC-003**: All authentication endpoint responses detailed in `spec.md` will accurately reflect the current backend behavior for signup and login.
-   **SC-004**: The `spec.md` will explicitly state if minimal responses are used for authentication endpoints.
-   **SC-005**: The `spec.md` will not introduce any new endpoints or fields, nor alter the existing structure or section order.