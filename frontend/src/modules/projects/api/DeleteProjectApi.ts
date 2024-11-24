import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';
import type { AxiosError } from 'axios';
import { useWorkspaceStore } from '@/modules/WorkSpaces/model/store/workSpaceStore';

// Функция удаления проекта
const deleteProject = async (projectId: number): Promise<void> => {
   await api.delete(`/projects/${projectId}`);
};

// Хук для удаления проекта
export const useDeleteProject = () => {
   const queryClient = useQueryClient();
   const currentWorkspaceId = useWorkspaceStore((state) => state.workspaces[0]?.id);

   return useMutation<void, AxiosError, number>({
      mutationFn: deleteProject,
      onSuccess: (_, projectId) => {
         console.log(`Проект с ID ${projectId} успешно удалён.`);
         // Инвалидируем кэш для обновления списка проектов текущего рабочего пространства
         queryClient.invalidateQueries(['projects', currentWorkspaceId]);
      },
      onError: (error) => {
         console.error('Ошибка при удалении проекта:', error.message);
      },
   });
};
