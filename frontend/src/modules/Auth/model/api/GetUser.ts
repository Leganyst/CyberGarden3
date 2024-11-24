import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';
import type { AxiosError } from 'axios';
import { useUserStore } from '../store/userStore';

interface IUser {
   name: string;
   email: string;
   id: number;
   created_at: string;
   updated_at: string;
}

const fetchUser = async (): Promise<IUser> => {
   const response = await api.get<IUser>('/auth/me');
   return response.data;
};

export const useFetchUser = () => {
   const setUserId = useUserStore((state) => state.setUserId);

   const queryResult = useQuery<IUser, AxiosError>({
      queryKey: ['user'],
      queryFn: fetchUser,
   });

   const { data, error, isSuccess, isError } = queryResult;

   useEffect(() => {
      if (isSuccess && data) {
         setUserId(data.id);
      }
   }, [isSuccess, data, setUserId]);

   useEffect(() => {
      if (isError && error) {
         console.error('Ошибка при получения данных:', error.message);
      }
   }, [isError, error]);

   return queryResult;
};
