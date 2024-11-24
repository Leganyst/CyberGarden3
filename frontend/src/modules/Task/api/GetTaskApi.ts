import { useQuery } from '@tanstack/react-query';
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

const fetchTaskById = async (taskId: number): Promise<Task> => {
   const response = await api.get<Task>(`/tasks/${taskId}`, {
      headers: {
         Accept: 'application/json',
      },
   });
   return response.data;
};

export const useFetchTaskById = (taskId: number) => {
   return useQuery<Task, AxiosError>({
      queryKey: ['task', taskId],
      queryFn: () => fetchTaskById(taskId),
      enabled: !!taskId,
   });
};
