import { api } from '@/shared/api/axios-instance';
import { IAuthResponse } from './types';
import { useTokenStore } from '../store/authStore';

export const refreshTokenRequest = async (): Promise<string | null> => {
   const { setAccessToken } = useTokenStore();
   try {
      const response = await api.get<IAuthResponse>('/auth/refresh');
      if (response.status >= 400) {
         throw new Error('Ошибка обновления токена');
      }
      const newToken = response.data.access_token;
      setAccessToken(newToken);
      return newToken;
   } catch (error) {
      console.error('Ошибка при обновлении токена:', error);
      localStorage.removeItem('token-storage'); // Очищаем токен при ошибке
      return null;
   }
};
