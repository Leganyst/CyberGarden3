import { useMutation } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';
import { AxiosError } from 'axios';

interface Task {
   name: string;
   due_date: string;
   priority: string;
   id: number;
   project_id: number;
   created_by: number;
   assigned_to: number | null;
   is_completed: boolean;
   created_at: string;
   updated_at: string;
}

interface UpdateTaskData {
   name?: string;
   due_date?: string;
   priority?: string;
   is_completed?: boolean;
   assigned_to?: number;
}

const updateTask = async (taskId: number, taskData: UpdateTaskData): Promise<Task> => {
   const response = await api.patch<Task>(`/tasks/${taskId}`, taskData, {
      headers: {
         Accept: 'application/json',
         'Content-Type': 'application/json',
      },
   });
   return response.data;
};

export const useUpdateTask = () => {
   return useMutation<Task, AxiosError, { taskId: number; taskData: UpdateTaskData }>({
      mutationFn: ({ taskId, taskData }) => updateTask(taskId, taskData),
      onSuccess: (updatedTask) => {
         console.log('Задача успешно обновлена:', updatedTask);
      },
      onError: (error) => {
         console.error('Ошибка при обновлении задачи:', error.message);
      },
   });
};
