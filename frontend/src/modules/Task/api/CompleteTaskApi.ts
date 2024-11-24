import { useMutation } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';
import { AxiosError } from 'axios';

interface Task {
   name: string;
   due_date: string;
   description: string | null;
   status: string;
   priority: string;
   id: number;
   project_id: number;
   created_by: number;
   assigned_to: number | null;
   is_completed: boolean;
   created_at: string;
   updated_at: string;
}

const updateTaskStatus = async (taskId: number, isCompleted: boolean): Promise<Task> => {
   const response = await api.patch<Task>(
      `/tasks/${taskId}/complete/${isCompleted}`,
      {},
      {
         headers: {
            Accept: 'application/json',
         },
      },
   );
   return response.data;
};

export const useUpdateTaskStatus = () => {
   return useMutation<Task, AxiosError, { taskId: number; isCompleted: boolean }>({
      mutationFn: ({ taskId, isCompleted }) => updateTaskStatus(taskId, isCompleted),
      onSuccess: (updatedTask) => {
         console.log('Статус задачи успешно обновлен:', updatedTask);
      },
      onError: (error) => {
         console.error('Ошибка при изменении статуса задачи:', error.message);
      },
   });
};
