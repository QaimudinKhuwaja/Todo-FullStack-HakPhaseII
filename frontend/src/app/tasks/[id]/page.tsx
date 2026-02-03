'use client';

import React, { useEffect } from 'react';
import { useParams } from 'next/navigation';
import { useTasks } from '@/hooks/useTasks';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import ErrorDisplay from '@/components/common/ErrorDisplay';
import TaskCard from '@/components/tasks/TaskCard';

const SingleTaskPage: React.FC = () => {
  const params = useParams();
  const taskId = params?.id ? parseInt(params.id as string, 10) : undefined;

  const {
    currentTask,
    isLoading,
    error,
    fetchTaskById,
    removeTask,
    updateExistingTask,
  } = useTasks();

  useEffect(() => {
    if (taskId) {
      fetchTaskById(taskId);
    }
  }, [taskId]);

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorDisplay message={error} />;
  if (!currentTask) return <ErrorDisplay message="Task not found." />;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Task Details</h1>

      <TaskCard
        task={currentTask}
        removeTask={removeTask}
        updateExistingTask={updateExistingTask}
        isLoading={isLoading}
      />
    </div>
  );
};

export default SingleTaskPage;
