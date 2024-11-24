import { api } from '@/shared/api/axios-instance';
import { useQuery } from '@tanstack/react-query';
import type { AxiosError } from 'axios';
import { useEffect } from 'react';

interface Project {
   created_at: string;
   created_by: number;
   id: number;
   name: string;
   updated_at: string;
   workspace_id: number;
}

const fetchProjectById = async (projectId: number): Promise<Project> => {
   const response = await api.get<Project>(`/projects/${projectId}`, {
      headers: {
         Accept: 'application/json',
      },
   });
   return response.data;
};

export const useFetchProjectById = (projectId: number) => {
   const queryResult = useQuery<Project, AxiosError>({
      queryKey: ['project', projectId],
      queryFn: () => fetchProjectById(projectId),
   });

   const { data, error, isSuccess, isError } = queryResult;

   // Дополнительная обработка данных проекта (если необходимо)
   useEffect(() => {
      if (isError && error) {
         console.error(`Ошибка при получении данных проекта ${projectId}:`, error.message);
      }
   }, [isError, error]);

   return queryResult;
};
