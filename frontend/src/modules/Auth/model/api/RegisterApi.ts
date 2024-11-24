// useRegister.ts
import { useMutation } from '@tanstack/react-query';
import type { IAuthResponse } from './types';
import type { AxiosError } from 'axios';
import { api } from '@/shared/api/axios-instance';
import { useTokenStore } from '../store/authStore';

interface RegisterCredentials {
   email: string;
   name: string;
   password: string;
}

const register = async (credentials: RegisterCredentials): Promise<IAuthResponse> => {
   const response = await api.post<IAuthResponse>('/auth/register', credentials);
   return response.data;
};

export const useRegister = () => {
   const { setAccessToken, setRefreshToken } = useTokenStore();

   return useMutation<IAuthResponse, AxiosError, RegisterCredentials>({
      mutationFn: register,
      onSuccess: (data) => {
         setAccessToken(data.access_token);
         setRefreshToken(data.refresh_token);
      },
      onError: (error) => {
         console.error('Ошибка при регистрации:', error.message);
      },
   });
};
