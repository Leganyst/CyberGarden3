import { Card, CardFooter, CardHeader } from '@/shared/ui/card';
import { Textarea } from '@/shared/ui/textarea';
import { AlarmClock, Calendar as CalendarIcon, Flag, User } from 'lucide-react';
import { TaskCommand } from './TaskCommand';
import type { ProjectItem } from './TaskComboBox';
import { TaskComboBox } from './TaskComboBox';
import { Button } from '@/shared/ui/button';
import { DatePicker } from './DatePicker';
import { DropdownMenuItem } from '@/shared/ui/dropdown-menu';
import type { ReactNode } from 'react';
import { useEffect, useState } from 'react';
import { useCreateTask } from '../api/CreateTaskApi';
import { useFetchProjectsByWorkspace } from '@/modules/projects/api/GetUserProjectsApi';

interface TaskProps {
   parentTask?: number;
   className?: string;
   setButtonClick?: (close: boolean) => void;
}
interface flag {
   flag: ReactNode;
   id: number;
   priority: string;
   value: string;
}
const flags: flag[] = [
   { id: 1, flag: <Flag className='mr-2 w-4' />, priority: 'Приоритет', value: 'None' },
   { id: 2, flag: <Flag className='mr-2 w-4 fill-red-600' />, priority: 'Высокий', value: 'high' },
   { id: 3, flag: <Flag className='mr-2 w-4 fill-yellow-400' />, priority: 'Средний', value: 'normal' },
   { id: 4, flag: <Flag className='mr-2 w-4 fill-blue-600' />, priority: 'Низкий', value: 'low' },
];
const users: ProjectItem[] = [
   {
      label: 'Пользователи',
      value: 'users',
      children: [
         { label: 'Вилков В. В. (240303vilkov@gmail.com)', value: 'Вилков В. В. (240303vilkov@gmail.com)' },
         { label: 'Макарычев И.И. (makar@gmail.com)', value: 'Макарычев И.И. (makar@gmail.com)' },
         { label: 'Марков А.П. (markov@gmail.com)', value: 'Марков А.П. (markov@gmail.com)' },
      ],
   },
];
interface Project {
   name: string;
   id: number;
   workspace_id: number;
   created_by: number;
   created_at: string;
   updated_at: string;
}
interface CreateTaskData {
   name: string; // Название задачи
   due_date: string; // Дата выполнения задачи в формате ISO (например, "2024-11-24T12:00:00Z")
   priority: string; // Приоритет задачи (например, "Высокий", "Средний", "Низкий")
   project_id: number; // Идентификатор проекта, к которому относится задача
   assigned_to: number | null; // Идентификатор пользователя, назначенного на задачу (или null)
   reminder_time: string; // Время напоминания в формате ISO (может быть пустой строкой, если не указано)
   created_by: number; // Идентификатор пользователя, создавшего задачу
   parent_task_id: number;
}

export const Task = ({
   className,
   setButtonClick,
   setModalOpen,
   parentTask,
}: TaskProps & { setModalOpen?: (isOpen: boolean) => void }) => {
   const { data: projects, isSuccess } = useFetchProjectsByWorkspace();
   const [name, setName] = useState('');
   const [description, setDescription] = useState('');
   const [dueDate, setDueDate] = useState<Date | undefined>();
   const [reminderTime, setReminderTime] = useState<Date | undefined>();
   const [project, setProject] = useState<ProjectItem | null>(null);
   const [assignedTo, setAssignedTo] = useState<ProjectItem | null>(null);
   const [priority, setPriority] = useState<flag>(flags[0]);

   const [projectItems, setProjectItems] = useState<ProjectItem[]>([]);

   const createTaskMutation = useCreateTask();

   // Преобразование проектов при успешной загрузке
   useEffect(() => {
      if (isSuccess && projects) {
         setProjectItems(mapProjectsToProjectItems(projects));
      }
   }, [isSuccess, projects]);

   const handleSubmit = () => {
      const taskData: CreateTaskData = {
         name,
         due_date: dueDate!.toLocaleDateString('en-CA'),
         priority: priority.value,

         project_id: project ? parseInt(project.value) : 0,
         assigned_to: assignedTo ? parseInt(assignedTo.value) : 0,
         reminder_time: reminderTime ? reminderTime.toISOString() : '',
         created_by: 1,
         parent_task_id: parentTask!,
      };

      createTaskMutation.mutate(taskData);
   };
   const isFormValid = () => {
      return name && project && dueDate && reminderTime;
   };

   useEffect(() => {
      if (createTaskMutation.isSuccess) {
         // Сброс формы
         setName('');
         setDescription('');
         setDueDate(undefined);
         setReminderTime(undefined);
         setProject(null);
         setAssignedTo(null);
         setPriority(flags[0]);

         // Закрытие модального окна
         if (setModalOpen) {
            setModalOpen(false);
         }
      }
   }, [createTaskMutation.isSuccess]);

   const mapProjectsToProjectItems = (projects: Project[]): ProjectItem[] => {
      return projects.map((project) => ({
         label: project.name,
         value: project.id.toString(),
      }));
   };

   return (
      <Card className='px-0 pb-0'>
         <CardHeader className='flex gap-4 pb-0 pt-0 md:flex-col esmob:px-2'>
            <Textarea
               className='my-4 h-12 border-none text-xl'
               placeholder='Название задачи'
               value={name}
               onChange={(e) => setName(e.target.value)}
            />
            <Textarea
               className='h-20 border-none'
               placeholder='Описание задачи'
               value={description}
               onChange={(e) => setDescription(e.target.value)}
            />
            <div className='flex flex-wrap gap-2'>
               <DatePicker
                  pickerName='Выберите дату выполнения задачи'
                  svg={<CalendarIcon className='mr-2 w-4' />}
                  selectedDate={dueDate}
                  onDateChange={setDueDate}
               />
               <TaskCommand svg={priority.flag} text={priority.priority}>
                  {flags.map((item) => (
                     <DropdownMenuItem key={item.id} className='flex' onClick={() => setPriority(item)}>
                        {item.flag} {item.priority}
                     </DropdownMenuItem>
                  ))}
               </TaskCommand>
               <DatePicker
                  pickerName='Выберите дату напоминания'
                  svg={<AlarmClock className='mr-2 w-4' />}
                  selectedDate={reminderTime}
                  onDateChange={setReminderTime}
               />
            </div>
         </CardHeader>
         <CardFooter className='lg:h-22 border-т flex flex-wrap items-center justify-between gap-4 py-3 esmob:justify-center'>
            <div className='ml-5 flex flex-wrap gap-2 esmob:ml-0'>
               {isSuccess && <TaskComboBox items={projectItems} onSelect={(value, label, item) => setProject(item)} />}

               <TaskComboBox
                  defaultLabel='Исполнитель'
                  items={users}
                  placeholder='Выберите пользователя'
                  svg={<User className='w-4' />}
                  onSelect={(value, label, item) => setAssignedTo(item)}
               />
            </div>

            <div className='flex gap-2 sm:mr-5 md:ml-5 md:mr-5 es:mx-5 esmob:mx-0 esmob:justify-center'>
               <Button
                  variant='ghost'
                  onClick={() => {
                     if (setModalOpen) {
                        setModalOpen(false); // Закрываем модальное окно
                     }
                  }}
               >
                  Отмена
               </Button>
               <Button disabled={!isFormValid()} onClick={handleSubmit}>
                  Добавить задачу
               </Button>
            </div>
         </CardFooter>
      </Card>
   );
};
