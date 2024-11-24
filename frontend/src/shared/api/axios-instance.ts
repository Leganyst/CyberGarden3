import { refreshTokenRequest } from '@/modules/Auth/model/api/refreshTokenRequest';
import { useTokenStore } from '@/modules/Auth/model/store/authStore';
import type { AxiosError, AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import axios from 'axios';
import * as decode from 'jwt-decode'; // Импортируем как модуль
const api: AxiosInstance = axios.create({
   baseURL: 'https://cybergarden.leganyst.ru',
   withCredentials: true,
   headers: {
      Accept: 'application/json', // Указываем ожидаемый формат ответа
   },
});

const onRequest = async (config: InternalAxiosRequestConfig): Promise<InternalAxiosRequestConfig> => {
   const { accessToken } = useTokenStore.getState(); // Get accessToken from the token store
   if (accessToken) {
      const decodedToken: { exp: number } = decode.jwtDecode(accessToken);
      console.log('Токен в onRequest:', accessToken);
      const currentDate = new Date();
      // console.log(decodedToken.exp * 1000 < currentDate.getTime())
      // console.log(decodedToken.exp * 1000 )
      // console.log(currentDate.getTime())
      if (decodedToken.exp * 1000 - 518000 < currentDate.getTime()) {
         const newToken = await refreshTokenRequest();
         if (newToken && !config.url?.includes('auth')) {
            config.headers.set('Authorization', `Bearer ${newToken}`);
         }
      } else {
         config.headers.set('Authorization', `Bearer ${accessToken}`);
      }
   }
   // Используем decode.default

   return config;
};

const onResponse = (response: AxiosResponse): AxiosResponse => response;
const onResponseError = (error: AxiosError): Promise<AxiosError> => Promise.reject(error);

api.interceptors.request.use(onRequest);
api.interceptors.response.use(onResponse, onResponseError);

export { api };
