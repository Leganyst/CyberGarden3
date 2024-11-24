import { useQuery } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';

import { useEffect } from 'react';
import type { AxiosError } from 'axios';
import { useTaskStore } from '@/modules/Task/model/store/TaskStore';
import { useProjectStore } from '../model/useProjectStore';

interface Task {
   name: string;
   due_date: string;
   description: string;
   status: string;
   priority: string;
   id: number;
   project_id: number;
   created_by: number;
   assigned_to: number | null;
   is_completed: boolean;
   created_at: string;
   updated_at: string;
   parent_task: Task | null;
   subtasks: Task[];
}

const fetchTasksByProject = async (projectId: number): Promise<Task[]> => {
   const response = await api.get<Task[]>(`/projects/${projectId}/tasks`, {
      headers: {
         Accept: 'application/json',
      },
   });
   return response.data;
};

export const useFetchTasksByProject = (projectId: number) => {
   const setTasks = useTaskStore((state) => state.setTasks);

   const queryResult = useQuery<Task[], AxiosError>({
      queryKey: ['tasks'],
      queryFn: () => fetchTasksByProject(projectId),
   });

   const { data, error, isSuccess, isError } = queryResult;

   useEffect(() => {
      if (isSuccess && data) {
         setTasks(data);
      }
   }, [isSuccess, data, setTasks]);

   useEffect(() => {
      if (isError && error) {
         console.error(`Ошибка при получении задач для проекта ${projectId}:`, error.message);
      }
   }, [isError, error]);

   return queryResult;
};
