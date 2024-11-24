import { useQuery } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';
import { AxiosError } from 'axios';

interface Reminder {
   id: number;
   content: string;
   created_at: string;
   updated_at: string;
}

const fetchUserReminders = async (): Promise<Reminder[]> => {
   const response = await api.get<Reminder[]>('/user/reminders', {
      headers: {
         Accept: 'application/json',
         Authorization: `Bearer YOUR_ACCESS_TOKEN_HERE`,
      },
   });
   return response.data;
};

export const useFetchUserReminders = () => {
   return useQuery<Reminder[], AxiosError>({
      queryKey: ['userReminders'],
      queryFn: fetchUserReminders,
   });
};
