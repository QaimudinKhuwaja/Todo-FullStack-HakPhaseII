// frontend/src/components/tasks/TaskList.tsx
'use client';

import React from 'react';
import { Task } from '@/types/task';
import TaskCard from './TaskCard';
import { useTasks } from '@/hooks/useTasks';

// const TaskList: React.FC = () => {
//   const { tasks, removeTask, updateExistingTask, isLoading } = useTasks();

//   if (!tasks || tasks.length === 0) {
//     return <p className="text-center text-gray-500">No tasks found.</p>;
//   }


  const TaskList: React.FC<{ tasks: Task[] }> = ({ tasks }) => {
  const { removeTask, updateExistingTask, isLoading } = useTasks();

  if (!tasks || tasks.length === 0) {
    return <p className="text-center text-gray-500">No tasks found.</p>;
  }

  return (
    <div>
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          removeTask={removeTask}
          updateExistingTask={updateExistingTask}
          isLoading={isLoading}
        />
      ))}
    </div>
  );
};

export default TaskList;
