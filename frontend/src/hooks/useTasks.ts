// src/app/hooks/useTasks.ts

'use client';

import { useState, useEffect } from 'react';
import { TaskEndpoints } from '@/lib/api/endpoints';
import { Task, TaskCreate, TaskUpdate } from '@/types/task';

export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [currentTask, setCurrentTask] = useState<Task | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const fetchedTasks = await TaskEndpoints.getAll();
      setTasks(fetchedTasks);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchTaskById = async (id: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const fetchedTask = await TaskEndpoints.getById(id);
      setCurrentTask(fetchedTask);
    } catch (err: any) {
      setError(err.message || `Failed to fetch task ${id}`);
    } finally {
      setIsLoading(false);
    }
  };

  const addTask = async (taskData: TaskCreate) => {
    setIsLoading(true);
    setError(null);
    try {
      const newTask = await TaskEndpoints.create(taskData);
      setTasks((prevTasks) => [...prevTasks, newTask]);
      return newTask;
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  const updateExistingTask = async (id: number, taskData: TaskUpdate) => {
    setIsLoading(true);
    setError(null);
    try {
      const updatedTask = await TaskEndpoints.update(id, taskData);
      setTasks((prevTasks) =>
        prevTasks.map((task) => (task.id === id ? updatedTask : task))
      );
      if (currentTask && currentTask.id === id) {
        setCurrentTask(updatedTask);
      }
      return updatedTask;
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  const removeTask = async (id: number) => {
  setIsLoading(true);
  setError(null);
  try {
    const res = await TaskEndpoints.delete(id);

    // ⭐ important: backend null / empty bhe bhej sakta
    if (res !== undefined) {
      setTasks((prevTasks) =>
        prevTasks.filter((task) => task.id !== id)
      );

      if (currentTask && currentTask.id === id) {
        setCurrentTask(null);
      }
      return true;
    }

    return false;
  } catch (err: any) {
    setError(err.message || 'Failed to delete task');
    return false;
  } finally {
    setIsLoading(false);
  }
};


  useEffect(() => {
    fetchTasks();
  }, []);

  return {
    tasks,
    currentTask,
    isLoading,
    error,
    fetchTasks,
    fetchTaskById,
    addTask,
    updateExistingTask,
    removeTask,
  };
};
