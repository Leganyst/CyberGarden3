import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';

interface Workspace {
   created_at: string;
   created_by: number;
   id: number;
   name: string;
   updated_at: string;
}

interface WorkspaceState {
   workspaces: Workspace[];
   addWorkspace: (workspace: Workspace) => void; // Добавить рабочее пространство
   clearWorkspaces: () => void; // Очистить список рабочих пространств
   getWorkspaceById: (id: number) => Workspace | undefined; // Получить рабочее пространство по ID
   removeWorkspace: (id: number) => void; // Удалить рабочее пространство по ID
   setWorkspaces: (workspaces: Workspace[]) => void; // Установить список рабочих пространств
   updateWorkspace: (updatedWorkspace: Workspace) => void; // Обновить рабочее пространство
}

export const useWorkspaceStore = create<WorkspaceState>()(
   persist(
      (set, get) => ({
         workspaces: [],

         setWorkspaces: (workspaces) => set({ workspaces }),

         addWorkspace: (workspace) =>
            set((state) => ({
               workspaces: [...state.workspaces, workspace],
            })),

         updateWorkspace: (updatedWorkspace) =>
            set((state) => ({
               workspaces: state.workspaces.map((workspace) =>
                  workspace.id === updatedWorkspace.id ? updatedWorkspace : workspace,
               ),
            })),

         removeWorkspace: (id) =>
            set((state) => ({
               workspaces: state.workspaces.filter((workspace) => workspace.id !== id),
            })),

         clearWorkspaces: () => set({ workspaces: [] }),

         getWorkspaceById: (id) => get().workspaces.find((workspace) => workspace.id === id),
      }),
      {
         name: 'workspace-storage',
         storage: createJSONStorage(() => localStorage),
      },
   ),
);
