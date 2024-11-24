import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';
import type { AxiosError } from 'axios';
import { useWorkspaceStore } from '@/modules/WorkSpaces/model/store/workSpaceStore';

interface CreateProjectData {
   created_by: number;
   name: string;
   workspace_id: number;
}

interface Project {
   created_at: string;
   created_by: number;
   id: number;
   name: string;
   updated_at: string;
   workspace_id: number;
}

const createProject = async (projectData: CreateProjectData): Promise<Project> => {
   const response = await api.post<Project>('/projects/', projectData);
   return response.data;
};

export const useCreateProject = () => {
   const queryClient = useQueryClient();
   const currentWorkspaceId = useWorkspaceStore((state) => state.workspaces[0]?.id);

   const mutation = useMutation<Project, AxiosError, CreateProjectData>({
      mutationFn: createProject,
      onSuccess: (newProject) => {
         // Инвалидируем кеш проектов для текущего рабочего пространства
         queryClient.invalidateQueries(['projects', currentWorkspaceId]);
      },
      onError: (error) => {
         console.error('Ошибка при создании проекта:', error.message);
      },
   });

   return mutation;
};
