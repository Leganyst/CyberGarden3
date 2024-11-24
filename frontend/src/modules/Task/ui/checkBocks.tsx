// Task.tsx

import React, { useEffect, useState } from 'react';
import { Plus, X } from 'lucide-react';

import { Checkbox } from '@/shared/ui/checkbox';
import { useTaskStore } from '../model/store/TaskStore';
import { CurrentTaskCard } from './currentTaskCard';
import { CreateTaskModal } from './CreateTaskModal';
import { useProjectStore } from '@/modules/projects/model/useProjectStore';
import { useFetchTasksByProject } from '@/modules/projects/api/GetProjectTasksApi';
import { TaskCommand } from './TaskCommand';
import { DropdownMenuItem } from '@/shared/ui/dropdown-menu';

interface Task {
   id: number;
   name: string;
   due_date: string;
   description: string | null;
   status: string;
   priority: string;
   project_id: number;
   created_by: number;
   assigned_to: number | null;
   is_completed: boolean;
   created_at: string;
   updated_at: string;
   parent_task: number | null;
   subtasks: Task[];
}

const statuses = [
   { id: 1, status: 'Открыто', color: 'bg-blue-400', icon: '🟦' },
   { id: 2, status: 'В работе', color: 'bg-yellow-400', icon: '🟨' },
   { id: 3, status: 'Проверка', color: 'bg-orange-400', icon: '🟧' },
   { id: 4, status: 'Готово', color: 'bg-green-400', icon: '🟩' },
];

function buildTaskTree(tasks: Task[]): Task[] {
   const taskMap = new Map<number, Task>();
   const rootTasks: Task[] = [];

   tasks.forEach((task) => {
      task.subtasks = [];
      taskMap.set(task.id, task);
   });

   tasks.forEach((task) => {
      if (task.parent_task) {
         const parentTask = taskMap.get(task.parent_task);
         if (parentTask) {
            parentTask.subtasks.push(task);
         }
      } else {
         rootTasks.push(task);
      }
   });

   return rootTasks;
}

const TaskItem: React.FC<{ task: Task; level: number }> = ({ task, level }) => {
   const { taskStates, setTaskChecked, updateTask, setSelectedTaskId } = useTaskStore();
   const currentProject = useProjectStore((state) => state.currentProject);
   const [currentStatus, setCurrentStatus] = useState(statuses.find((item) => item.status === task.status) || statuses[0]);

   useEffect(() => {
      // Устанавливаем статус задачи с сервера при загрузке компонента
      const initialStatus = statuses.find((item) => item.status === task.status) || statuses[0];
      setCurrentStatus(initialStatus);
   }, [task.status]);

   const handleCheckboxChange = (checked: boolean) => {
      setTaskChecked(task.id, checked);
      updateTask({ ...task, is_completed: checked });
   };

   const handleTaskClick = () => {
      setSelectedTaskId(task.id);
   };

   const handleStatusChange = async (newStatus: (typeof statuses)[number]) => {
      try {
         // Здесь выполняем запрос на сервер для обновления статуса задачи
         await updateTask({ ...task, status: newStatus.status });
         setCurrentStatus(newStatus); // Локально обновляем статус
      } catch (error) {
         console.error('Ошибка при обновлении статуса задачи:', error);
      }
   };

   return (
      <div
         className={`my-2 ${level === 0 ? 'border-y' : 'border-none'} py-2`}
         onClick={handleTaskClick}
         style={{ marginLeft: level * 20 }} // Отступ для подзадач
      >
         <div className='relative flex h-10 items-center space-x-2'>
            <Checkbox
               checked={taskStates[task.id] || false}
               className='h-6 w-6'
               id={`${task.id}`}
               onCheckedChange={handleCheckboxChange}
            />
            <label
               className='text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70'
               htmlFor={`${task.id}`}
               onClick={(e) => e.preventDefault()}
            >
               <CreateTaskModal
                  buttonChildren={task.name}
                  buttonClassName='custom-button-class'
                  closeClassName='absolute right-2 top-2 rounded-sm'
                  closeIcon={<X className='h-4 w-4' />}
                  modalClassName='p-0'
                  overlayClassName='bg-black/15'
               >
                  <CurrentTaskCard />
               </CreateTaskModal>
            </label>
            <TaskCommand svg={currentStatus.color} text={currentStatus.status} rounded={true} btnWidth={'w-5'}>
               {statuses.map((item) => (
                  <DropdownMenuItem
                     key={item.id}
                     className='flex cursor-pointer items-center p-2 hover:bg-gray-200'
                     onClick={() => handleStatusChange(item)}
                  >
                     <div className={`mr-2 h-3 w-3 rounded-full ${item.color}`} />
                     {item.status}
                  </DropdownMenuItem>
               ))}
            </TaskCommand>

            <div className='absolute right-3 text-gray-400'>{currentProject?.name}</div>
         </div>

         {task.subtasks && task.subtasks.map((subTask) => <TaskItem key={subTask.id} level={level + 1} task={subTask} />)}
      </div>
   );
};

export function CheckboxTask() {
   const { setTaskChecked, selectedTaskId, getTaskById, tasks } = useTaskStore();
   const { selectedProjectId } = useProjectStore();

   const { data: fetchedTasks, isLoading, isError } = useFetchTasksByProject(selectedProjectId!);

   const [taskTree, setTaskTree] = useState<Task[]>([]);

   useEffect(() => {
      if (fetchedTasks) {
         fetchedTasks.forEach((task) => {
            setTaskChecked(task.id, task.is_completed);
         });

         // Построение дерева задач
         const rootTasks = buildTaskTree(fetchedTasks);
         setTaskTree(rootTasks);
      }
   }, [fetchedTasks, setTaskChecked]);

   if (isLoading) return <div>Загрузка задач...</div>;
   if (isError) return <div>Ошибка при загрузке задач</div>;

   const selectedTask = selectedTaskId ? getTaskById(selectedTaskId) : null;

   return (
      <div>
         <div>
            {taskTree.map((task) => (
               <TaskItem key={task.id} level={0} task={task} />
            ))}
         </div>
      </div>
   );
}
