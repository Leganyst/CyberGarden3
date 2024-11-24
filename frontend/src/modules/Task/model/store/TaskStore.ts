import { create } from 'zustand';

interface Task {
   assigned_to: number | null; // ID пользователя, которому назначена задача
   created_at: string;
   created_by: number;
   description: string;
   due_date: string; // Дата выполнения задачи в формате ISO
   id: number;
   is_completed: boolean;
   name: string;
   parent_task_id: number;
   priority: string; // Приоритет задачи (например, "Высокий", "Средний", "Низкий")
   project_id: number; // ID проекта, к которому относится задача
   reminder_time?: string | null; // Время напоминания в формате ISO (опционально)
   status: string;
   subtasks: Task[]; // Подзадачи
   updated_at: string;
}

interface TaskState {
   selectedTaskId: number | null; // ID выбранной задачи
   tasks: Task[]; // Список задач
   taskStates: Record<number, boolean>; // Состояния задач (например, чекбоксы)
   addSubtask: (parentId: number, subtask: Task) => void; // Добавление подзадачи
   addTask: (task: Task) => void; // Добавление задачи
   clearTasks: () => void; // Очистка всех задач
   getTaskById: (id: number) => Task | undefined; // Получение задачи по ID
   removeSubtask: (parentId: number, subtaskId: number) => void; // Удаление подзадачи
   removeTask: (id: number) => void; // Удаление задачи
   setSelectedTaskId: (id: number) => void; // Установка выбранной задачи
   setTaskChecked: (id: number, isChecked: boolean) => void; // Установка состояния задачи
   setTasks: (tasks: Task[]) => void; // Установка всех задач
   toggleTaskCompletion: (id: number) => void; // Переключение состояния задачи
   updateSubtask: (parentId: number, updatedSubtask: Task) => void; // Обновление подзадачи
   updateTask: (updatedTask: Task) => void; // Обновление задачи
}

export const useTaskStore = create<TaskState>()((set, get) => ({
   tasks: [],
   taskStates: {},
   selectedTaskId: null, // Изначально задача не выбрана

   // Установить список задач
   setTasks: (tasks) => set({ tasks }),

   // Добавить новую задачу
   addTask: (task) =>
      set((state) => ({
         tasks: [...state.tasks, task],
      })),

   // Добавить подзадачу
   addSubtask: (parentId, subtask) =>
      set((state) => ({
         tasks: state.tasks.map((task) =>
            task.id === parentId ? { ...task, subtasks: [...(task.subtasks || []), subtask] } : task,
         ),
      })),

   // Обновить существующую задачу
   updateTask: (updatedTask) =>
      set((state) => ({
         tasks: state.tasks.map((task) => (task.id === updatedTask.id ? updatedTask : task)),
      })),

   // Обновить подзадачу
   updateSubtask: (parentId, updatedSubtask) =>
      set((state) => ({
         tasks: state.tasks.map((task) =>
            task.id === parentId
               ? {
                    ...task,
                    subtasks: task.subtasks.map((subtask) => (subtask.id === updatedSubtask.id ? updatedSubtask : subtask)),
                 }
               : task,
         ),
      })),

   // Переключить состояние выполнения задачи
   toggleTaskCompletion: (id) =>
      set((state) => ({
         tasks: state.tasks.map((task) => (task.id === id ? { ...task, is_completed: !task.is_completed } : task)),
      })),

   // Удалить задачу
   removeTask: (id) =>
      set((state) => ({
         tasks: state.tasks.filter((task) => task.id !== id),
      })),

   // Удалить подзадачу
   removeSubtask: (parentId, subtaskId) =>
      set((state) => ({
         tasks: state.tasks.map((task) =>
            task.id === parentId
               ? {
                    ...task,
                    subtasks: task.subtasks.filter((subtask) => subtask.id !== subtaskId),
                 }
               : task,
         ),
      })),

   // Установить состояние задачи (например, чекбокса)
   setTaskChecked: (id, isChecked) =>
      set((state) => ({
         taskStates: { ...state.taskStates, [id]: isChecked },
      })),

   // Установить ID выбранной задачи
   setSelectedTaskId: (id) => set({ selectedTaskId: id }),

   // Получить задачу по ID
   getTaskById: (id) => get().tasks.find((task) => task.id === id),

   // Очистить все задачи и их состояния
   clearTasks: () => set({ tasks: [], taskStates: {}, selectedTaskId: null }),
}));
