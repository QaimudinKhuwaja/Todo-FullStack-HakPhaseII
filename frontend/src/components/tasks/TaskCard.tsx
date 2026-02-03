// // frontend/src/components/tasks/TaskCard.tsx
// 'use client';

// import React, { useState } from 'react';
// import { Task } from '@/types/task';
// import { useTasks } from '@/hooks/useTasks';
// import TaskForm from './TaskForm';
// import DeleteConfirmationModal from './DeleteConfirmationModal';
// import { useRouter } from 'next/navigation';

// interface TaskCardProps {
//   task: Task;
// }

// const TaskCard: React.FC<TaskCardProps> = ({ task }) => {
//   const [isEditing, setIsEditing] = useState(false);
//   const [showDeleteModal, setShowDeleteModal] = useState(false);
//   const { updateExistingTask, removeTask, isLoading } = useTasks();
//   const router = useRouter();

//   const handleUpdate = async (updatedData: Partial<Task>) => {
//     await updateExistingTask(task.id, updatedData);
//     setIsEditing(false);
//   };

//   const handleDelete = async () => {
//     await removeTask(task.id);
//     setShowDeleteModal(false);
//     // Optionally redirect or refresh if on a single task page
//     // if (router.pathname === `/tasks/${task.id}`) {
//     //   router.push('/dashboard');
//     // }
//   };

//   const handleToggleStatus = async () => {
//     const newStatus = task.status === 'pending' ? 'completed' : 'pending';
//     await updateExistingTask(task.id, { status: newStatus });
//   };

//   return (
//     <div className="bg-white shadow-md rounded-lg p-4 mb-4">
//       {isEditing ? (
//         <TaskForm
//           initialData={task}
//           onSubmit={handleUpdate}
//           onCancel={() => setIsEditing(false)}
//         />
//       ) : (
//         <>
//           <h3 className="text-xl font-bold">{task.title}</h3>
//           <p className="text-gray-600">{task.description}</p>
//           <div className="mt-2 flex items-center">
//             <span
//               className={`px-2 py-1 text-sm font-semibold rounded-full ${
//                 task.status === 'completed' ? 'bg-green-200 text-green-800' : 'bg-yellow-200 text-yellow-800'
//               }`}
//             >
//               {task.status}
//             </span>
//             <button
//               onClick={handleToggleStatus}
//               className="ml-4 bg-blue-500 hover:bg-blue-700 text-white text-sm py-1 px-3 rounded"
//               disabled={isLoading}
//             >
//               Mark as {task.status === 'pending' ? 'Completed' : 'Pending'}
//             </button>
//           </div>
//           <div className="mt-4">
//             <button
//               onClick={() => setIsEditing(true)}
//               className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mr-2"
//             >
//               Edit
//             </button>
//             <button
//               onClick={() => setShowDeleteModal(true)}
//               className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
//             >
//               Delete
//             </button>
//           </div>
//         </>
//       )}

//       <DeleteConfirmationModal
//         isOpen={showDeleteModal}
//         onClose={() => setShowDeleteModal(false)}
//         onConfirm={handleDelete}
//         isLoading={isLoading}
//       />
//     </div>
//   );
// };

// export default TaskCard;




// src/app/components/tasks/TaskCard.tsx
'use client';

import React, { useState } from 'react';
import { Task } from '@/types/task';
import { useTasks } from '@/hooks/useTasks';
import TaskForm from './TaskForm';
import DeleteConfirmationModal from './DeleteConfirmationModal';
import { useRouter } from 'next/navigation';

interface TaskCardProps {
  task: Task;
  removeTask: (id: number) => Promise<boolean>;
  updateExistingTask: (id: number, data: any) => Promise<any>;
  isLoading: boolean;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, removeTask, updateExistingTask, isLoading }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const router = useRouter();

  // ✅ UPDATE TASK
  const handleUpdate = async (updatedData: Partial<Task>) => {
    try {
      const res = await updateExistingTask(task.id, updatedData);
      if (res) {
        setIsEditing(false);
        router.refresh();
      }
    } catch (error) {
      console.error('Update Error:', error);
    }
  };

  // ✅ DELETE TASK (FIXED)
  const handleDelete = async () => {
  console.log("HANDLE DELETE RUN");
  console.log("Task ID:", task.id);

  await removeTask(task.id);

  console.log("DELETE API DONE");

  setShowDeleteModal(false);
};

  // ✅ TOGGLE STATUS (FIXED)
 const [localStatus, setLocalStatus] = useState(task.status);

const handleToggleStatus = async () => {
  try {
    const newStatus = localStatus === 'pending' ? 'completed' : 'pending';
    await updateExistingTask(task.id, { status: newStatus });
    setLocalStatus(newStatus); // ✅ Update local state for instant UI change
  } catch (err) {
    console.error('Status Update Error:', err);
  }
};


  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-4">
      {isEditing ? (
        <TaskForm
          initialData={task}
          onSubmit={handleUpdate}
          onCancel={() => setIsEditing(false)}
        />
      ) : (
        <>
          <h3 className="text-xl font-bold">{task.title}</h3>
          <p className="text-gray-600">{task.description}</p>

          {/* STATUS */}
      <span
  className={`px-2 py-1 text-sm font-semibold rounded-full ${
    localStatus === 'completed'
      ? 'bg-green-200 text-green-800'
      : 'bg-yellow-200 text-yellow-800'
  }`}
>
  {localStatus}
</span>

<button
  onClick={handleToggleStatus}
  className="ml-4 bg-blue-500 hover:bg-blue-700 text-white text-sm py-1 px-3 rounded disabled:opacity-50"
  disabled={isLoading}
>
  Mark as {localStatus === 'pending' ? 'Completed' : 'Pending'}
</button>


          {/* ACTION BUTTONS */}
          <div className="mt-4">
            <button
              onClick={() => setIsEditing(true)}
              className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mr-2"
            >
              Edit
            </button>

           <button
  onClick={handleDelete}
  className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
>
  Delete
</button>


          </div>
        </>
      )}

      <DeleteConfirmationModal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onConfirm={handleDelete}
        isLoading={isLoading}
      />
    </div>
  );
};

export default TaskCard;
