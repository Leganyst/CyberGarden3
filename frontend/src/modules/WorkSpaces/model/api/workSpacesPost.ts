import { useMutation } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';
import type { AxiosError } from 'axios';
import { useTokenStore } from '@/modules/Auth/model/store/authStore';
import { useWorkspaceStore } from '../store/workSpaceStore';

interface CreateWorkspaceData {
   created_by: number;
   name: string;
}

interface Workspace {
   owner_id: number;
   workspace_name: string;
}

const createWorkspace = async (workspaceData: CreateWorkspaceData): Promise<Workspace> => {
   const response = await api.post<Workspace>('/workspaces/', workspaceData);
   return response.data;
};

export const useCreateWorkspace = () => {
   return useMutation<Workspace, AxiosError, CreateWorkspaceData>({
      mutationFn: createWorkspace,
      onSuccess: (newWorkspace) => {
         console.log('Воркспейс успешно создан:', newWorkspace);
      },
      onError: (error) => {
         console.error('Ошибка при создании воркспейса:', error.message);
      },
   });
};
