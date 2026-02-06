// //lib/api/endpoints.ts
// import { api } from './client';
// import { User, AuthResponse } from '@/types/auth';
// import { Task, TaskCreate, TaskUpdate } from '@/types/task';

// /* =========================
//    AUTH ENDPOINTS
// ========================= */

// export const AuthEndpoints = {
//   register: (userData: any) =>
//     api.post<User>('/users/', userData),

//   // ✅ LOGIN JSON BODY
//   login: (loginData: any) =>
//     api.post<AuthResponse>('/login', loginData),

//   logout: () =>
//     api.post<void>('/logout', {}),

//   me: () =>
//     api.get<User>('/users/me'),

//   protected: () =>
//     api.get<any>('/protected'),
// };

// /* =========================
//    TASK ENDPOINTS
// ========================= */

// export const TaskEndpoints = {
//   create: (taskData: TaskCreate) =>
//     api.post<Task>('/tasks/', taskData),

//   getAll: () =>
//     api.get<Task[]>('/tasks/'),

//   getById: (taskId: number) =>
//     api.get<Task>(`/tasks/${taskId}`),

//   update: (taskId: number, taskData: TaskUpdate) =>
//     api.patch<Task>(`/tasks/${taskId}`, taskData),

//   delete: (taskId: number) =>
//     api.delete<void>(`/tasks/${taskId}`),
// };

// /* =========================
//    SYSTEM ENDPOINTS
// ========================= */

// export const SystemEndpoints = {
//   health: () => api.get<string>('/health'),
//   root: () => api.get<string>('/'),
// };



















// //lib/api/endpoints.ts
// import { api } from './client';
// import { User, AuthResponse } from '@/types/auth';
// import { Task, TaskCreate, TaskUpdate } from '@/types/task';

// /* =========================
//    AUTH ENDPOINTS
// ========================= */

// export const AuthEndpoints = {
//   register: (userData: any) =>
//     api.post<User>('/users', userData),

//   // ✅ LOGIN JSON BODY
//   login: (loginData: any) =>
//     api.post<AuthResponse>('/login', loginData),

//   logout: () =>
//     api.post<void>('/logout', {}),

//   me: () =>
//     api.get<User>('/users/me'),

//   protected: () =>
//     api.get<any>('/protected'),
// };

// /* =========================
//    TASK ENDPOINTS
// ========================= */

// export const TaskEndpoints = {
//   create: (taskData: TaskCreate) =>
//     api.post<Task>('/tasks', taskData),

//   getAll: () =>
//     api.get<Task[]>('/tasks'),

//   getById: (taskId: number) =>
//     api.get<Task>(`/tasks/${taskId}`),

//   update: (taskId: number, taskData: TaskUpdate) =>
//     api.patch<Task>(`/tasks/${taskId}`, taskData),

//   delete: (taskId: number) =>
//     api.delete<void>(`/tasks/${taskId}`),
// };

// /* =========================
//    SYSTEM ENDPOINTS
// ========================= */

// export const SystemEndpoints = {
//   health: () => api.get<string>('/health'),
//   root: () => api.get<string>('/'),
// };




// lib/api/endpoints.ts
import { api } from './client';
import { User, AuthResponse } from '@/types/auth';
import { Task, TaskCreate, TaskUpdate } from '@/types/task';

/* =========================
   AUTH ENDPOINTS
========================= */

export const AuthEndpoints = {
  register: (userData: any) =>
    api.post<User>('/users', userData),  // no trailing /

  login: (loginData: any) =>
    api.post<AuthResponse>('/login', loginData),

  logout: () =>
    api.post<void>('/logout', {}),

  me: () =>
    api.get<User>('/users/me'),

  protected: () =>
    api.get<any>('/protected'),
};

/* =========================
   TASK ENDPOINTS
========================= */

export const TaskEndpoints = {
  create: (taskData: TaskCreate) =>
    api.post<Task>('/tasks', taskData),

  getAll: () =>
    api.get<Task[]>('/tasks'),

  getById: (taskId: number) =>
    api.get<Task>(`/tasks/${taskId}`),

  update: (taskId: number, taskData: TaskUpdate) =>
    api.patch<Task>(`/tasks/${taskId}`, taskData),

  delete: (taskId: number) =>
    api.delete<void>(`/tasks/${taskId}`),
};

/* =========================
   SYSTEM ENDPOINTS
========================= */

export const SystemEndpoints = {
  health: () => api.get<string>('/health'),
  root: () => api.get<string>('/'),
};