import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const fetchSchedule = async (group: string) => {
   const response = await axios.get(`https://webictis.sfedu.ru/schedule-api/?query=${group}`);
   return response.data;
};

export const useSchedule = (group: string) => {
   return useQuery({
      queryKey: ['schedule', group], // Ключ для кэширования
      queryFn: () => fetchSchedule(group), // Функция запроса
      enabled: !!group, // Запрос отправляется только если указана группа
      staleTime: 5 * 60 * 1000, // Данные считаются свежими 5 минут
   });
};
