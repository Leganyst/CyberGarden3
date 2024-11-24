import { useQuery } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';
import { AxiosError } from 'axios';

// Интерфейс комментария
interface Comment {
   content: string;
   id: number;
   task_id: number;
   user_id: number;
   created_at: string;
   updated_at: string;
}

// Функция для получения комментариев задачи
const fetchTaskComments = async (taskId: number): Promise<Comment[]> => {
   const response = await api.get<{ comments: Comment[] }>(`/tasks/${taskId}/comments`, {
      headers: {
         Accept: 'application/json',
         Authorization: `Bearer YOUR_ACCESS_TOKEN_HERE`, // Укажите ваш токен
      },
   });
   return response.data.comments;
};

// Хук для получения комментариев задачи
export const useFetchTaskComments = (taskId: number) => {
   return useQuery<Comment[], AxiosError>({
      queryKey: ['taskComments', taskId], // Ключ кэша для этой задачи
      queryFn: () => fetchTaskComments(taskId),
      enabled: !!taskId, // Выполнять запрос только если taskId существует
   });
};
