// frontend/src/app/dashboard/page.tsx
'use client';

import React, { useEffect } from 'react';
import { useTasks } from '@/hooks/useTasks';
import TaskList from '@/components/tasks/TaskList';
import TaskForm from '@/components/tasks/TaskForm';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import ErrorDisplay from '@/components/common/ErrorDisplay';

const DashboardPage: React.FC = () => {
  const { tasks, isLoading, error, fetchTasks, addTask } = useTasks();

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleCreateTask = async (data: any) => {
    await addTask(data);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Your Tasks</h1>
      <ErrorDisplay message={error} />
      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <>
          <div className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Create New Task</h2>
            <TaskForm onSubmit={handleCreateTask} />
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-4">All Tasks</h2>
            <TaskList tasks={tasks} />
          </div>
        </>
      )}
    </div>
  );
};

export default DashboardPage;
