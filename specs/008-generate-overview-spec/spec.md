# Feature Specification: Project Overview and System Audit

**Feature Branch**: `008-generate-overview-spec`  
**Created**: 2026-02-07
**Status**: Draft
**Input**: User description: "You are working on a Spec-Kit Plus spec-driven monorepo project. IMPORTANT RULES: - This project already has a working full-stack Todo app - DO NOT modify existing code architecture - Only document and map current system into specs - Future chatbot must integrate WITHOUT breaking current system Project Stack (Already Implemented): Frontend: Next.js (App Router, TypeScript, Tailwind) Backend: FastAPI ORM: SQLModel Database: Neon PostgreSQL Auth: Better Auth (planned or partial) Existing Features: - Full CRUD Todo - Multi user structure - REST API already exists - Database already connected TASK: Generate a SPEC FILE named: specs/overview.md Include: 1️⃣ Project Purpose Todo app evolving into AI chatbot task manager 2️⃣ Current System Audit Document: - Existing frontend structure - Existing backend routes - Database schema (tasks) - Current auth flow status 3️⃣ Phase Mapping Phase II → Web App (Already built) Phase III → AI Chatbot (To build) 4️⃣ Integration Rules - Existing APIs remain unchanged - Chatbot will reuse existing CRUD APIs OR DB layer - No breaking changes allowed 5️⃣ High Level Architecture Include layered diagram explanation (text based) 6️⃣ Risks and Constraints - Must remain stateless - Must maintain user isolation - Must use JWT verification Output clean spec-kit style markdown."

## 1. Project Purpose

The primary purpose of this project is to serve as a full-stack Todo application that is being evolved into an AI-powered chatbot task manager. This document provides an overview of the current system architecture to guide future development and integration of the AI chatbot functionality.

## 2. Current System Audit

This section documents the existing components of the full-stack application.

### Frontend Structure

The frontend is a Next.js application using the App Router, TypeScript, and Tailwind CSS. The main application structure is located in `frontend/src/app` and includes the following key directories:

-   **/app/(auth)/**: Contains pages related to user authentication (login, register).
-   **/app/dashboard/**: The main user dashboard after login.
-   **/app/tasks/**: Likely contains pages for viewing, creating, and editing tasks.
-   **/app/page.tsx**: The main landing page.
-   **/app/layout.tsx**: The root layout for the application.

### Backend Routes

The backend is a FastAPI application. The main API endpoints are defined by including routers in `backend/app/main.py`. The existing API is organized as follows:

-   **/health**: Endpoints for health checks.
-   **/users**: Endpoints for user management (e.g., creating users).
-   **/auth**: Endpoints for handling user authentication (e.g., login, token generation).
-   **/protected**: Example protected endpoints that require authentication.
-   **/tasks**: Endpoints for CRUD operations on tasks.

### Database Schema

The database uses PostgreSQL, and the schema is managed via SQLModel.

#### `User` Model

-   `id` (int, primary key)
-   `email` (str, unique)
-   `password_hash` (str)
-   `is_active` (bool)

#### `Task` Model

-   `id` (int, primary key)
-   `title` (str)
-   `description` (str, optional)
-   `completed` (bool)
-   `owner_id` (int, foreign key to `user.id`)
-   `created_at` (datetime)
-   `updated_at` (datetime)

### Authentication Flow

The current authentication flow is based on JWTs. The status is partially implemented ("Better Auth (planned or partial)").
1.  User registers or logs in via the `/auth` endpoints.
2.  The backend provides a JWT access token.
3.  The frontend stores this token and includes it in the `Authorization` header for requests to protected endpoints.
4.  The backend verifies the JWT to authorize requests.

## 3. Phase Mapping

-   **Phase II → Web App (Already built)**: The current full-stack Todo application.
-   **Phase III → AI Chatbot (To build)**: The next phase of development, which will introduce an AI chatbot for task management.

## 4. Integration Rules

-   **Existing APIs remain unchanged**: The current REST API for tasks and users must not have breaking changes.
-   **Chatbot Reuse**: The future AI chatbot will reuse the existing CRUD APIs for tasks or interact with the database layer directly.
-   **No Breaking Changes**: All new development must be backward compatible with the existing web application.

## 5. High-Level Architecture

The system follows a classic layered architecture.

```
+---------------------+
|      Frontend       | (Next.js, React, Tailwind)
+---------------------+
          | (REST API over HTTPS)
+---------------------+
|      Backend        | (FastAPI, Python)
+---------------------+
          | (SQLAlchemy Core)
+---------------------+
|      Database       | (PostgreSQL)
+---------------------+
```

-   **Presentation Layer (Frontend)**: A Next.js single-page application that provides the user interface.
-   **Application/API Layer (Backend)**: A FastAPI server that exposes a RESTful API for all business logic (task management, user authentication).
-   **Data Access Layer (ORM)**: SQLModel acts as the ORM, translating Python objects to database rows.
-   **Data Persistence Layer (Database)**: A Neon PostgreSQL database stores all user and task data.

## 6. Risks and Constraints

-   **Statelessness**: The backend must remain stateless, with all client state managed by the frontend.
-   **User Isolation**: Data must be strictly isolated between users. All database queries must be scoped to the authenticated user's ID.
-   **JWT Verification**: All protected endpoints must robustly verify the JWT signature and claims.

## User Scenarios & Testing

### User Story 1 - Developer Onboarding (Priority: P1)

As a new developer joining the project, I want to read a single document that gives me a complete overview of the existing architecture so that I can quickly understand the system and start contributing to Phase III.

**Acceptance Scenarios**:

1.  **Given** I have access to the codebase, **When** I read this specification, **Then** I can identify the key technologies, the overall structure, and the existing features without needing to inspect every file.

## Success Criteria

### Measurable Outcomes

-   **SC-001**: A new developer can explain the high-level architecture and data models after reading this document.
-   **SC-002**: This document is used as the primary reference for planning the integration of the Phase III AI Chatbot.