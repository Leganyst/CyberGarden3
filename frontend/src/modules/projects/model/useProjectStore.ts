import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';

interface Project {
   created_at: string;
   created_by: number;
   id: number;
   name: string;
   updated_at: string;
   workspace_id: number;
}

interface ProjectState {
   currentProject: Project | null;
   projects: Project[];
   workspaceProjects: Project[]; // Список проектов текущего рабочего пространства
   selectedProjectId: number | null; // ID выбранного проекта

   addProject: (project: Project) => void;
   clearProjects: () => void;
   filterProjectsByWorkspace: (workspaceId: number) => void; // Метод фильтрации
   removeProject: (id: number) => void;
   setCurrentProject: (project: Project | null) => void;
   setProjects: (projects: Project[]) => void;
   toggleCurrentProject: (id: number) => void;
   updateProject: (updatedProject: Project) => void;
   setSelectedProjectId: (id: number | null) => void; // Устанавливает ID выбранного проекта
}

export const useProjectStore = create<ProjectState>()((set, get) => ({
   projects: [],
   currentProject: null,
   selectedProjectId: null,
   workspaceProjects: [], // Изначально пустой список

   setProjects: (projects) => {
      set({ projects });
   },

   setCurrentProject: (project) => {
      set({ currentProject: project });
   },
   setSelectedProjectId: (id) => {
      set({ selectedProjectId: id });
   },

   addProject: (project) => {
      set((state) => ({
         projects: [...state.projects, project],
      }));
   },

   removeProject: (id) => {
      set((state) => ({
         projects: state.projects.filter((proj) => proj.id !== id),
      }));
   },

   updateProject: (updatedProject) => {
      set((state) => ({
         projects: state.projects.map((proj) => (proj.id === updatedProject.id ? updatedProject : proj)),
      }));
   },

   toggleCurrentProject: (id) => {
      set((state) => {
         const project = state.projects.find((proj) => proj.id === id);
         return {
            currentProject: state.currentProject?.id === id ? null : project || null,
         };
      });
   },

   clearProjects: () => {
      set({ projects: [], currentProject: null, workspaceProjects: [] });
   },

   filterProjectsByWorkspace: (workspaceId) => {
      const allProjects = get().projects;
      const filteredProjects = allProjects.filter((proj) => proj.workspace_id === workspaceId);
      set({ workspaceProjects: filteredProjects });
   },
}));
