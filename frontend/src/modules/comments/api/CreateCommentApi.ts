import { useMutation } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';
import { AxiosError } from 'axios';

interface Comment {
   content: string;
   id: number;
   task_id: number;
   user_id: number;
   created_at: string;
   updated_at: string;
}

interface CreateCommentData {
   content: string;
   task_id: number;
}

const createTaskComment = async (commentData: CreateCommentData): Promise<Comment> => {
   const response = await api.post<Comment>('/comments/', commentData, {
      headers: {
         Accept: 'application/json',
         Authorization: `Bearer YOUR_ACCESS_TOKEN_HERE`,
         'Content-Type': 'application/json',
      },
   });
   return response.data;
};

export const useCreateTaskComment = () => {
   return useMutation<Comment, AxiosError, CreateCommentData>({
      mutationFn: createTaskComment,
      // onSuccess: (newComment) => {
      //    console.log('Комментарий успешно создан:', newComment);
      // },
      onError: (error) => {
         console.error('Ошибка при создании комментария:', error.message);
      },
   });
};
