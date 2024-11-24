import { useMutation } from '@tanstack/react-query';
import { api } from '@/shared/api/axios-instance';
import { AxiosError } from 'axios';
import { useTaskStore } from '@/modules/Task/model/store/TaskStore';
import { queryClient } from '@/shared/api/query-client';

interface CreateTaskData {
   name: string; // Название задачи
   due_date: string; // Дата выполнения задачи в формате ISO (например, "2024-11-24T12:00:00Z")
   priority: string; // Приоритет задачи (например, "Высокий", "Средний", "Низкий")
   project_id: number; // Идентификатор проекта, к которому относится задача
   assigned_to: number | null; // Идентификатор пользователя, назначенного на задачу (или null)
   reminder_time: string; // Время напоминания в формате ISO (может быть пустой строкой, если не указано)
   created_by: number; // Идентификатор пользователя, создавшего задачу
}

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
   parent_task_id: number;
}

const createTask = async (taskData: CreateTaskData): Promise<Task> => {
   const response = await api.post<Task>('/tasks/', taskData, {
      headers: {
         Accept: 'application/json',
         'Content-Type': 'application/json',
      },
   });
   return response.data;
};

export const useCreateTask = () => {
   const addTask = useTaskStore((state) => state.addTask);

   return useMutation<Task, AxiosError, CreateTaskData>({
      mutationFn: createTask,
      onSuccess: (newTask) => {
         console.log('Задача успешно создана:', newTask);
         addTask(newTask); // Добавляем задачу в Zustand
         queryClient.invalidateQueries(['tasks']);
      },
      onError: (error) => {
         console.error('Ошибка при создании задачи:', error.message);
      },
   });
};
