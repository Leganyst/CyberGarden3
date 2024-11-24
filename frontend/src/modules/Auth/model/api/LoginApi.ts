import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import type { AxiosError } from 'axios';
import axios from 'axios';

import type { IAuthResponse } from './types';
import { api } from '@/shared/api/axios-instance';
import { useTokenStore } from '../store/authStore';

interface LoginCredentials {
   email: string;
   password: string;
}

const login = async (credentials: LoginCredentials): Promise<IAuthResponse> => {
   const response = await api.post<IAuthResponse>(
      `/auth/login`,
      {
         ...credentials,
      },
      {
         headers: {
            Accept: 'application/json',
         },
      },
   );

   if (response.status >= 400) {
      throw new Error('Ошибка авторизации');
   }

   return response.data;
};

export const useLogin = () => {
   const { setAccessToken, setRefreshToken } = useTokenStore();

   return useMutation<IAuthResponse, AxiosError, LoginCredentials>({
      mutationFn: login,
      onSuccess: (data) => {
         localStorage.clear();
         setAccessToken(data.access_token);
         setRefreshToken(data.refresh_token);
      },
      onError: (error) => {
         console.error('Ошибка при входе в систему:', error);
      },
   });
};
