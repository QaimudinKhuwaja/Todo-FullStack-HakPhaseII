// frontend/src/types/task.ts

export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: 'pending' | 'completed';
  owner_id: number;
}

export interface TaskCreate {
  title: string;
  description?: string;
  status?: 'pending' | 'completed';
}

export interface TaskUpdate {
  title?: string;
  description?: string | null;
  status?: 'pending' | 'completed';
}