### Frontend UI Implementation Plan for Feature `007-frontend-ui-spec`

**Project Stack:**
*   **Frontend:** Next.js 16+ (App Router)
*   **Styling:** Tailwind CSS
*   **Backend:** FastAPI
*   **Auth:** Token-based authentication
*   **Database:** Neon PostgreSQL (via backend only)

---

### 1️⃣ Folder Structure (Next.js App Router)

The project will adhere to the standard Next.js App Router conventions, organized for modularity and maintainability.

```
src/
├── app/                  # Main application routes and layout
│   ├── (auth)/           # Route Group for authentication-related pages
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   ├── dashboard/        # Protected dashboard page
│   │   └── page.tsx
│   ├── tasks/
│   │   ├── [id]/         # Dynamic route for task detail/edit
│   │   │   └── page.tsx
│   │   └── page.tsx      # Optional: if a root /tasks page is needed, otherwise directly under dashboard
│   ├── layout.tsx        # Root layout for the application
│   ├── page.tsx          # Home page (e.g., redirect to login if unauthenticated)
│   └── globals.css       # Global styles (Tailwind base)
├── components/           # Reusable UI components
│   ├── auth/             # Authentication-related components
│   │   ├── AuthForm.tsx
│   │   └── LogoutButton.tsx
│   ├── common/           # General-purpose UI components
│   │   ├── Navbar.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── ErrorDisplay.tsx
│   ├── tasks/            # Task-specific components
│   │   ├── TaskCard.tsx
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   └── DeleteConfirmationModal.tsx
│   └── ui/               # Lower-level UI primitives (e.g., Button, Input if custom)
├── lib/                  # Utility functions and API client
│   ├── api/              # API client and service definitions
│   │   ├── client.ts     # Centralized API client (fetch/Axios instance)
│   │   └── endpoints.ts  # Endpoint definitions and request functions
│   ├── auth/             # Authentication utilities
│   │   ├── token.ts      # Token storage and retrieval functions
│   │   └── middleware.ts # Client-side authentication middleware/helpers
│   └── utils.ts          # General utility functions
├── types/                # TypeScript type definitions
│   ├── auth.ts
│   └── tasks.ts
├── hooks/                # Custom React hooks (e.g., for data fetching, state management)
│   ├── useAuth.ts
│   └── useTasks.ts
└── styles/               # Tailwind CSS configuration and additional styles
    └── tailwind.config.ts
```

---

### 2️⃣ Routing Plan

The routing will leverage Next.js App Router's file-system based routing and route groups for better organization.

| UI Route               | Backend Endpoint Usage                                  | Protection                                         | Redirection (Unauthenticated)         |
| :--------------------- | :------------------------------------------------------ | :------------------------------------------------- | :------------------------------------ |
| `/`                    | None (redirects to `/login` if unauthenticated)       | Public (handles redirection)                       | `/login`                              |
| `/register`            | `POST /users/`                                          | Public                                             | None                                  |
| `/login`               | `POST /login`                                           | Public                                             | None                                  |
| `/dashboard`           | `GET /tasks/`                                           | Protected                                          | `/login`                              |
| `/tasks/[id]`          | `GET /tasks/{task_id}`, `PATCH /tasks/{task_id}`, `DELETE /tasks/{task_id}` | Protected                                          | `/login`                              |
| (API-driven 401)       | Any protected backend endpoint                          | N/A (handled by API client/middleware)             | `/login`                              |

**Next.js Middleware:** A `middleware.ts` file at the project root will be used to protect routes and redirect unauthenticated users to `/login`. It will check for the presence of the authentication token (e.g., in cookies).

---

### 3️⃣ Component Architecture

Components will be designed for reusability and clear separation of concerns.

-   **AuthForm (components/auth/AuthForm.tsx):**
    -   **Responsibility:** Handles user input for login and registration.
    -   **Props:** `type: 'login' | 'register'`, `onSubmit: (credentials) => void`, `isLoading: boolean`, `error: string`.
    -   **Backend Integration:** Calls `lib/api/endpoints.ts` for `POST /users/` or `POST /login`.

-   **Navbar (components/common/Navbar.tsx):**
    -   **Responsibility:** Navigation links (Dashboard), displays user status (e.g., "Logged in as User X"), and includes a Logout button.
    -   **Props:** `isLoggedIn: boolean`, `onLogout: () => void`.
    -   **Backend Integration:** Calls `lib/api/endpoints.ts` for `POST /logout` via `LogoutButton`.

-   **TaskList (components/tasks/TaskList.tsx):**
    -   **Responsibility:** Fetches and displays a list of `TaskCard` components.
    -   **Props:** None (fetches data internally or via a custom hook).
    -   **Backend Integration:** Calls `lib/api/endpoints.ts` for `GET /tasks/`.
    -   **State Management:** Manages its own loading, error, and task list state.

-   **TaskCard (components/tasks/TaskCard.tsx):**
    -   **Responsibility:** Displays a single task's title, description, and completion status. Provides actions (edit, delete).
    -   **Props:** `task: TaskType`, `onEdit: (taskId) => void`, `onDelete: (taskId) => void`, `onToggleComplete: (taskId) => void`.
    -   **Backend Integration:** Triggers parent component/hook to call `PATCH /tasks/{task_id}` or `DELETE /tasks/{task_id}`.

-   **TaskForm (components/tasks/TaskForm.tsx):**
    -   **Responsibility:** Handles input for creating new tasks or editing existing ones.
    -   **Props:** `initialTask?: TaskType`, `onSubmit: (taskData) => void`, `isLoading: boolean`, `error: string`.
    -   **Backend Integration:** Calls `lib/api/endpoints.ts` for `POST /tasks/` or `PATCH /tasks/{task_id}`.

-   **DeleteConfirmationModal (components/tasks/DeleteConfirmationModal.tsx):**
    -   **Responsibility:** Provides a confirmation dialog before task deletion.
    -   **Props:** `isOpen: boolean`, `onConfirm: () => void`, `onCancel: () => void`.

-   **LoadingSpinner (components/common/LoadingSpinner.tsx):**
    -   **Responsibility:** Generic loading indicator.
    -   **Props:** None.

-   **ErrorDisplay (components/common/ErrorDisplay.tsx):**
    -   **Responsibility:** Generic error message display.
    -   **Props:** `message: string`.

---

### 4️⃣ State Management Plan

State management will primarily rely on React's built-in `useState` and `useContext` for local component state and global shared state where appropriate. For data fetching, custom hooks will encapsulate the logic.

-   **Authentication State:**
    -   **Location:** `useAuth.ts` hook or a dedicated `AuthContext` (if more global access is needed beyond simple checks).
    -   **Contents:** `isLoggedIn: boolean`, `token: string | null`, `user: UserType | null`, `login: (token) => void`, `logout: () => void`.
    -   **Storage:** The token will be stored in an `httpOnly` cookie on the client-side for enhanced security, managed by the API client and Next.js middleware. A simple check for its presence will determine `isLoggedIn`.

-   **Task State:**
    -   **Location:** Primarily within page components (e.g., `/dashboard/page.tsx`, `/tasks/[id]/page.tsx`) using `useState`.
    -   **For list of tasks:** `/dashboard/page.tsx` will fetch and manage the list of tasks.
    -   **For single task:** `/tasks/[id]/page.tsx` will fetch and manage the details of a specific task.
    -   **Data Synchronization:** After CUD operations (Create, Update, Delete) on tasks, the UI will be updated by refetching the task list or directly modifying the local state, depending on the complexity and real-time requirements. Server-side rendering (SSR) or incremental static regeneration (ISR) for tasks could be considered for performance, but initially, client-side fetching with revalidation will suffice.

-   **Loading and Error States:**
    -   Each component making an API call will manage its own `isLoading` and `error` states using `useState`.
    -   Global error handling (e.g., 401 redirection) will be managed by the API client and Next.js middleware.

---

### 5️⃣ API Layer Plan

A centralized API client will abstract away API request details, ensuring consistency and reusability.

-   **API Client (`lib/api/client.ts`):**
    -   Uses `fetch` (or a lightweight library like `ky` or `axios` if required, but `fetch` is preferred for minimal dependencies).
    -   **Base URL:** Configured via `NEXT_PUBLIC_API_BASE_URL` environment variable.
    -   **Request Interceptors:**
        -   Attaches `Authorization: Bearer <token>` header for all protected requests. The token will be read from the `httpOnly` cookie.
        -   Sets `Content-Type: application/json`.
    -   **Response Interceptors:**
        -   Parses JSON responses.
        -   Handles network errors.
        -   **Specifically handles 401 (Unauthorized) responses by redirecting to `/login`**.
        -   Throws custom error types for API errors to be caught by UI components.

-   **Endpoint Definitions (`lib/api/endpoints.ts`):**
    -   Provides functions for each backend API endpoint.
    -   Example: `login(credentials)`, `register(userData)`, `getTasks()`, `createTask(taskData)`, `getTask(taskId)`, `updateTask(taskId, taskData)`, `deleteTask(taskId)`, `logout()`.
    -   Each function will call the central API client.

```typescript
// lib/api/client.ts
import { redirect } from 'next/navigation';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

interface ApiOptions extends RequestInit {
  token?: string; // Will be read from httpOnly cookie on backend for SSR/middleware, or directly from client for CSR
}

async function apiFetch<T>(url: string, options: ApiOptions = {}): Promise<T> {
  const { token, headers, ...rest } = options;

  const res = await fetch(`${API_BASE_URL}${url}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...headers,
    },
    ...rest,
  });

  if (res.status === 401) {
    // Client-side redirection for unauthorized access
    // This needs careful handling in Next.js App Router, potentially via a global error handler or specific page logic.
    // For now, redirect will be handled by middleware on server, or by client-side logic on specific API calls.
    redirect('/login'); // This works only in Server Components or within a 'use client' component with router.push
    throw new Error('Unauthorized'); // Propagate error for client-side handling
  }

  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || 'An API error occurred');
  }

  return res.json() as Promise<T>;
}

export const API = {
  get: <T>(url: string, options?: ApiOptions) => apiFetch<T>(url, { method: 'GET', ...options }),
  post: <T>(url: string, data: any, options?: ApiOptions) => apiFetch<T>(url, { method: 'POST', body: JSON.stringify(data), ...options }),
  patch: <T>(url: string, data: any, options?: ApiOptions) => apiFetch<T>(url, { method: 'PATCH', body: JSON.stringify(data), ...options }),
  delete: <T>(url: string, options?: ApiOptions) => apiFetch<T>(url, { method: 'DELETE', ...options }),
};
```
*(Note: The `redirect('/login')` in `apiFetch` might not work directly in all client-side contexts within the App Router and will require careful integration with `next/navigation`'s `useRouter` or a global error boundary for consistent behavior. The primary 401 handling will be via Next.js middleware for initial route protection.)*

---

### 6️⃣ Auth Integration Plan

Authentication will be token-based, using JWTs issued by the backend, with security considerations for token storage and protected routes.

-   **Token Storage Strategy:**
    -   The backend `/login` endpoint will return an `httpOnly` cookie containing the JWT. This prevents client-side JavaScript from accessing the token, mitigating XSS attacks.
    -   For server-side operations (middleware, Server Components), the token will be automatically sent with requests to the backend.
    -   For client-side API calls, the browser will automatically include the `httpOnly` cookie.

-   **Auth Middleware Strategy (`middleware.ts`):**
    -   A Next.js middleware will run on every request to check for the presence and validity of the authentication cookie/token for protected routes.
    -   If the token is missing or invalid for a protected route, the middleware will redirect the user to `/login`.
    -   Routes like `/login`, `/register`, and `/` (if it redirects) will be excluded from authentication checks.

-   **Protected Route Strategy:**
    -   All routes under `/dashboard`, `/tasks` will be considered protected.
    -   The `middleware.ts` will enforce authentication for these paths.
    -   Individual page components (e.g., `/dashboard/page.tsx`) will also perform client-side checks for authentication status and handle redirects if direct access occurs (e.g., by a user trying to bypass middleware via client-side routing after token expiry).

---

### 7️⃣ Data Flow Plan

The data flow will be unidirectional, initiated by user actions and flowing through the UI, API layer, backend, and then updating the UI.

1.  **User Action:** User interacts with UI (e.g., clicks "Login", "Create Task").
2.  **UI Component:** The relevant UI component (e.g., `AuthForm`, `TaskForm`) captures the input/event.
3.  **API Call:** The UI component (or an associated hook/page) dispatches a call to the `lib/api/endpoints.ts` functions.
4.  **API Client:** The `lib/api/client.ts` prepares the request, adds necessary headers (e.g., Authorization token from cookie), and sends it to the backend.
5.  **Backend (FastAPI):**
    -   Receives the request.
    -   Authenticates the request (JWT validation).
    -   Processes the request (e.g., interacts with PostgreSQL via SQLModel).
    -   Sends a response (data or error).
6.  **API Client:** Receives the response, handles common concerns (e.g., 401 redirection), and parses the data or error.
7.  **UI Update:** The UI component receives the processed data or error.
    -   On success: Updates its local state, which re-renders the UI (e.g., new task in list, dashboard view, redirection).
    -   On error: Displays an error message using `ErrorDisplay` component.
    -   During request: Displays `LoadingSpinner` component.

---

### 8️⃣ Error Handling Plan

Comprehensive error handling will be implemented at multiple levels to provide a robust user experience.

-   **401 (Unauthorized) Redirection:**
    -   **Primary:** Next.js `middleware.ts` will catch unauthenticated access to protected routes and redirect to `/login`.
    -   **Secondary:** The `lib/api/client.ts` will intercept 401 responses from any API call and trigger a client-side redirect to `/login` (or invalidate token and reload page to trigger middleware).
    -   **Message:** No explicit error message is displayed, as redirection is the expected behavior.

-   **API Error Display:**
    -   Any other `res.ok` (non-2xx) response from the backend will result in an error being thrown by `lib/api/client.ts`.
    -   UI components will catch these errors (e.g., in `try/catch` blocks or via error handling in custom hooks).
    -   The `ErrorDisplay` component will be used to show user-friendly error messages extracted from the API response (e.g., `errorData.detail`).

-   **Loading States:**
    -   Each API call will be associated with a `isLoading` state in the component or hook initiating the request.
    -   The `LoadingSpinner` component will be rendered conditionally based on this `isLoading` state.

-   **Validation Errors:**
    -   Client-side form validation (e.g., for empty task title) will be performed before sending API requests.
    -   Error messages will be displayed inline next to the form fields using simple conditional rendering.
    -   Backend validation errors (returned as API errors) will be handled as general API errors.

---

### 9️⃣ Security Plan

Security considerations are paramount, especially concerning authentication tokens and data access.

-   **Token Protection:**
    -   JWTs will be stored in `httpOnly` cookies, preventing client-side JavaScript access and reducing XSS vulnerability.
    -   Cookies will be set with `Secure` and `SameSite=Strict` attributes to protect against CSRF and man-in-the-middle attacks where possible.

-   **No DB Direct Access:**
    -   Strictly enforced that the frontend will ONLY communicate with the FastAPI backend via the defined API endpoints.
    -   No direct connections, queries, or exposure of database credentials from the frontend.

-   **Secure Headers Usage:**
    -   The Next.js application will leverage Next.js's built-in security headers (e.g., Content Security Policy, X-Content-Type-Options) to enhance overall application security. Configuration will be via `next.config.js`.

-   **Environment Variable Security:**
    -   `NEXT_PUBLIC_API_BASE_URL` is a public environment variable, but sensitive information (like API keys if any were introduced) would NOT be exposed as `NEXT_PUBLIC_`.
    -   Backend authentication secrets will remain server-side only.

---

### 🔟 Implementation Order

A phased approach to implementation will ensure steady progress and allow for early testing of core functionalities.

**Phase 1: Setup & Core Authentication Flow**
1.  Initialize Next.js project with Tailwind CSS.
2.  Configure `NEXT_PUBLIC_API_BASE_URL` environment variable.
3.  Implement `lib/api/client.ts` and `lib/api/endpoints.ts` for authentication endpoints (`/users/`, `/login`, `/logout`).
4.  Create `/app/(auth)/login/page.tsx` and `/app/(auth)/register/page.tsx` with `AuthForm` components.
5.  Implement `middleware.ts` for route protection and 401 redirection.
6.  Implement basic `/app/page.tsx` to redirect to `/login` if unauthenticated, or `/dashboard` if authenticated.
7.  Test User Registration and Login user flows (User Story 1).

**Phase 2: Task Management - Display & Creation**
1.  Implement `lib/api/endpoints.ts` for `GET /tasks/` and `POST /tasks/`.
2.  Create `TaskCard`, `TaskList`, and `TaskForm` components.
3.  Implement `/app/dashboard/page.tsx` to display tasks using `TaskList` and allow task creation using `TaskForm`.
4.  Test task listing and creation (partial User Story 2).

**Phase 3: Task Management - Detail, Update & Delete**
1.  Implement `lib/api/endpoints.ts` for `GET /tasks/{task_id}`, `PATCH /tasks/{task_id}`, `DELETE /tasks/{task_id}`.
2.  Implement `/app/tasks/[id]/page.tsx` for task detail and editing using `TaskForm`.
3.  Implement `DeleteConfirmationModal`.
4.  Integrate update and delete functionality into `TaskCard` and `/app/tasks/[id]/page.tsx`.
5.  Test task detail, update, and delete user flows (remainder of User Story 2).

**Phase 4: Polish & Refinements**
1.  Implement `Navbar` with Logout functionality.
2.  Refine error handling and loading states with `LoadingSpinner` and `ErrorDisplay` components across the application.
3.  Implement client-side form validations.
4.  Ensure visual consistency with Tailwind CSS, responsiveness (FR-021, FR-022).
5.  Visually distinguish completed tasks (FR-023).
6.  Perform final testing against all User Stories and Acceptance Scenarios.

---

**Constitution Check:**

-   **Mandatory Development Workflow:** This plan strictly adheres to Spec → Plan → Tasks → Implement.
-   **Allowed Technology Stack:** Uses Next.js (App Router), TypeScript, Tailwind CSS, and FastAPI. Token-based authentication is consistent with "Better Auth" concept.
-   **Disallowed Technologies:** No additional authentication libraries, ORMs, or state management beyond React defaults are planned. No direct frontend-to-database access. Session-based authentication is not used on backend.
-   **Security Principles:** All backend API endpoints are assumed to require JWT auth, frontend derives identity from JWT. Data operations are scoped to authenticated user implicitly by backend design.
-   **Project Structure:** Monorepo with frontend/backend folders. Specs are under `/specs`.
-   **Implementation Authority:** This plan is generated by Gemini CLI.
-   **Success Criteria:** The plan addresses all functional requirements and user stories, and aims to meet measurable outcomes.

---

**Output Artifacts:**

-   **IMPL_PLAN:** `specs/007-frontend-ui-spec/plan.md` (this document)

---

**Next Steps (Handoffs):**

-   **Create Tasks:** Break this plan into detailed implementation tasks. Run `sp.tasks` on this plan.
-   **Create Checklist:** Create a checklist for security policies, API contracts, or component review.