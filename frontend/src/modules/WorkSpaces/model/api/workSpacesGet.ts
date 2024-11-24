import type { UseQueryOptions } from '@tanstack/react-query';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';
import type { AxiosError } from 'axios';
import { useWorkspaceStore } from '../store/workSpaceStore';

interface IWorkspace {
   created_at: string;
   created_by: number;
   id: number;
   name: string;
   updated_at: string;
}

export const useFetchWorkspacesAsync = (options?: UseQueryOptions<IWorkspace[], AxiosError>) => {
   const setWorkspaces = useWorkspaceStore((state) => state.setWorkspaces);

   const fetchWorkspaces = async (): Promise<IWorkspace[]> => {
      const response = await api.get<IWorkspace[]>('/workspaces/');
      setWorkspaces(response.data);
      return response.data;
   };

   return useQuery<IWorkspace[], AxiosError>({
      queryKey: ['workspaces'],
      queryFn: fetchWorkspaces,
      enabled: false,
      ...options,
   });
};
