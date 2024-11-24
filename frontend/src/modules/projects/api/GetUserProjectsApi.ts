import { useQuery } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';
import { useEffect } from 'react';

import type { AxiosError } from 'axios';
import { useProjectStore } from '../model/useProjectStore';
import { useWorkspaceStore } from '@/modules/WorkSpaces/model/store/workSpaceStore';

interface Project {
   created_at: string;
   created_by: number;
   id: number;
   name: string;
   updated_at: string;
   workspace_id: number;
}

const fetchProjectsByWorkspace = async (workspaceId: number): Promise<Project[]> => {
   const response = await api.get<Project[]>(`/projects/${workspaceId}/all`, {
      headers: {
         Accept: 'application/json',
      },
   });
   return response.data;
};

export const useFetchProjectsByWorkspace = () => {
   const setProjects = useProjectStore((state) => state.setProjects);
   const currentWorkspaceId = useWorkspaceStore((state) => state.workspaces[0]?.id);

   const queryResult = useQuery<Project[], AxiosError>({
      queryKey: ['projects', currentWorkspaceId],
      queryFn: () => fetchProjectsByWorkspace(currentWorkspaceId!),
      enabled: !!currentWorkspaceId,
   });

   const { data, error, isSuccess, isError } = queryResult;

   useEffect(() => {
      if (isSuccess && data) {
         setProjects(data);
      }
   }, [isSuccess, data, setProjects]);

   useEffect(() => {
      if (isError && error) {
         console.error(`Ошибка при получении проектов для рабочего пространства ${currentWorkspaceId}:`, error.message);
      }
   }, [isError, error, currentWorkspaceId]);

   return queryResult;
};
