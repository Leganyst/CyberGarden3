import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';
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

interface UpdateProjectData {
   name?: string;
}

const updateProject = async ({ id, name }: { id: number; name: string }): Promise<void> => {
   await api.patch(`/projects/${id}`, { name });
};

export const useUpdateProject = () => {
   const queryClient = useQueryClient();
   const currentWorkspaceId = useWorkspaceStore((state) => state.workspaces[0]?.id);

   return useMutation<void, AxiosError, { id: number; name: string }>({
      mutationFn: updateProject,
      onSuccess: (_, { id }) => {
         console.log(`Проект с ID ${id} успешно обновлён.`);
         queryClient.invalidateQueries(['projects', currentWorkspaceId]);
      },
      onError: (error) => {
         console.error('Ошибка при обновлении проекта:', error.message);
      },
   });
};
