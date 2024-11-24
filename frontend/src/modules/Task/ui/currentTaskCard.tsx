import { Card, CardContent, CardFooter, CardHeader } from '@/shared/ui/card';
import { Textarea } from '@/shared/ui/textarea';
import { AlarmClock, Calendar as CalendarIcon, Flag as FlagIcon, Plus, User, X } from 'lucide-react';
import { TaskCommand } from './TaskCommand';
import { TaskComboBox } from './TaskComboBox';
import { Button } from '@/shared/ui/button';
import { DatePicker } from './DatePicker';
import { DropdownMenuItem } from '@/shared/ui/dropdown-menu';
import { useTaskStore } from '../model/store/TaskStore';
import { useEffect, useState } from 'react';
import { Title } from '@/shared/ui/title';
import { Input } from '@/shared/ui/input';
import { Task } from './Task';

interface CurrentTaskCardProps {
   className?: string;
}

interface Flag {
   className: string;
   id: number;
   priority: string;
}

const usersData = [
   { label: 'Вилков В. В. (240303vilkov@gmail.com)', value: 'Вилков В. В. (240303vilkov@gmail.com)', role: 'Пользователь' },
   { label: 'Козлов А. А. (kozlov@example.com)', value: 'Козлов А. А. (kozlov@example.com)', role: 'Администратор' },
   { label: 'Семенова И. И. (semenova@example.com)', value: 'Семенова И. И. (semenova@example.com)', role: 'Менеджер' },
];

const flags: Flag[] = [
   { id: 1, className: 'mr-2 w-4', priority: 'Приоритет' },
   { id: 2, className: 'mr-2 w-4 fill-red-600', priority: 'Высокий' },
   { id: 3, className: 'mr-2 w-4 fill-yellow-400', priority: 'Средний' },
   { id: 4, className: 'mr-2 w-4 fill-blue-600', priority: 'Низкий' },
];

interface Subtask {
   completed: boolean;
   id: number;
   name: string;
}

export const CurrentTaskCard = ({ className }: CurrentTaskCardProps) => {
   const { selectedTaskId, getTaskById, updateTask } = useTaskStore();
   const task = getTaskById(selectedTaskId || 0);
   const [closeSubTuskCreate, setCloseSubTuskCreate] = useState<boolean>(false);
   const [currentFlag, setCurrentFlag] = useState<Flag>(flags[0]);
   const [dueDate, setDueDate] = useState<Date | undefined>();
   const [reminderDate, setReminderDate] = useState<Date | undefined>();
   const [project, setProject] = useState<string | null>(null);
   const [isAddingSubtask, setIsAddingSubtask] = useState(false);
   const [newSubtaskName, setNewSubtaskName] = useState('');
   const [selectedUsers, setSelectedUsers] = useState<string[]>([]);

   useEffect(() => {
      if (task) {
         setCurrentFlag(flags.find((flag) => flag.priority === task.priority) || flags[0]);
         setDueDate(task.due_date ? new Date(task.due_date) : undefined);
         setReminderDate(task.reminder_time ? new Date(task.reminder_time) : undefined);
         setProject(task.project_id ? task.project_id.toString() : null);
         setIsAddingSubtask(false);
         setNewSubtaskName('');
         setSelectedUsers(task.assigned_to || []);
      }
   }, [task]);

   const handleFlagSelect = (selectedFlag: Flag) => {
      setCurrentFlag(selectedFlag);
      if (task) {
         updateTask({ ...task, priority: selectedFlag.priority });
      }
   };

   const handleDateChange = (field: 'due_date' | 'reminder_time', date: Date | undefined) => {
      if (task) {
         updateTask({ ...task, [field]: date ? date.toISOString() : null });
      }
   };

   const handleProjectSelect = (value: string) => {
      setProject(value);
      if (task) {
         updateTask({ ...task, project_id: Number.parseInt(value) });
      }
   };

   const handleAddUser = (value: string) => {
      if (!selectedUsers.includes(value)) {
         const updatedUsers = [...selectedUsers, value];
         setSelectedUsers(updatedUsers);
         if (task) {
            updateTask({ ...task, assigned_to: updatedUsers });
         }
      }
   };

   const handleRemoveUser = (user: string) => {
      const updatedUsers = selectedUsers.filter((selectedUser) => selectedUser !== user);
      setSelectedUsers(updatedUsers);
      if (task) {
         updateTask({ ...task, assigned_to: updatedUsers });
      }
   };

   const handleAddSubtask = () => {
      if (task && newSubtaskName.trim() !== '') {
         const newSubtask: Subtask = {
            id: Date.now(),
            name: newSubtaskName,
            completed: false,
         };
         const updatedTask = {
            ...task,
            subtasks: [...(task.subtasks || []), newSubtask],
         };
         updateTask(updatedTask);
         setNewSubtaskName('');
         setIsAddingSubtask(false);
      }
   };

   if (!task) {
      return <div>Задача не выбрана</div>;
   }

   return (
      <Card className='flex h-screen flex-col px-0 pb-0 lg:h-auto'>
         <CardHeader className='ml-4 mt-3 flex flex-wrap justify-between border-b p-0 sm:h-10 lg:h-10'>
            {task.name || 'Название задачи'}
         </CardHeader>
         <CardContent className='flex h-full flex-col gap-4 overflow-y-auto pb-0 pt-0 lg:h-auto lg:flex-row'>
            {/* Левая колонка */}
            <div className='flex flex-1 flex-col gap-4 pb-0 pt-0'>
               <h2 className='text-lg sm:text-xl'>{task.name}</h2>
               <Textarea
                  className='border-none'
                  placeholder='Описание задачи'
                  value={task.description}
                  onChange={(e) => updateTask({ ...task, description: e.target.value })}
               />
               {task.subtasks && task.subtasks.length > 0 && (
                  <div className='subtasks-list'>
                     {task.subtasks.map((subtask) => (
                        <div key={subtask.id} className='flex items-center gap-2'>
                           <input
                              checked={subtask.is_completed}
                              type='checkbox'
                              onChange={() => {
                                 const updatedSubtasks = task.subtasks.map((s) =>
                                    s.id === subtask.id ? { ...s, completed: !s.is_completed } : s,
                                 );
                                 updateTask({ ...task, subtasks: updatedSubtasks });
                              }}
                           />
                           <span className={subtask.is_completed ? 'line-through' : ''}>{subtask.name}</span>
                        </div>
                     ))}
                  </div>
               )}
               {isAddingSubtask ? (
                  <Task parentTask={task.id} setButtonClick={() => setCloseSubTuskCreate(false)} />
               ) : (
                  <Button
                     className='my-4 flex h-10 w-full justify-start text-sm font-medium lg:text-base'
                     variant='ghost'
                     onClick={() => setIsAddingSubtask(true)}
                  >
                     <div className='flex gap-2'>
                        <Plus className='text-primary' />
                        Добавить подзадачу
                     </div>
                  </Button>
               )}
            </div>

            {/* Правая колонка */}
            <div className='min-w-full rounded-lg bg-accent p-4 lg:min-w-80'>
               <div className='flex flex-col gap-3'>
                  <Title className='text-sm font-medium lg:text-base' text='Проект' />
                  <TaskComboBox
                     items={[
                        { label: 'Учёба', value: '1' },
                        { label: 'Работа', value: '2' },
                     ]}
                     btnWidth='h-12'
                     className='w-full'
                     onSelect={(value) => handleProjectSelect(value)}
                  />
                  <Title className='text-sm font-medium lg:text-base' text='Срок' />
                  <DatePicker
                     className='h-10 w-full sm:h-12'
                     pickerName='Выберите дату выполнения задания'
                     selectedDate={task.due_date ? new Date(task.due_date) : undefined}
                     svg={<CalendarIcon className='mr-2 w-4' />}
                     onDateChange={(date) => handleDateChange('due_date', date)}
                  />
                  <Title className='text-sm font-medium lg:text-base' text='Приоритет' />
                  <TaskCommand
                     slot
                     btnWidth='h-10 sm:h-12'
                     className='flex w-full justify-between'
                     svg={<FlagIcon className={currentFlag.className} />}
                     text={currentFlag.priority}
                  >
                     {flags.map((item) => (
                        <DropdownMenuItem key={item.id} className='flex' onClick={() => handleFlagSelect(item)}>
                           <FlagIcon className={item.className} /> {item.priority}
                        </DropdownMenuItem>
                     ))}
                  </TaskCommand>
                  <Title className='text-sm font-medium lg:text-base' text='Напоминание' />
                  <DatePicker
                     className='h-10 w-full sm:h-12'
                     pickerName='Выберите дату напоминаний'
                     selectedDate={task.reminder_time ? new Date(task.reminder_time) : undefined}
                     svg={<AlarmClock className='mr-2 w-4' />}
                     onDateChange={(date) => handleDateChange('reminder_time', date)}
                  />
                  <Title className='text-sm font-medium lg:text-base' text='Исполнители' />
                  <TaskComboBox
                     items={[
                        {
                           label: 'Пользователи',
                           value: 'users',
                           children: usersData.map((user) => ({
                              label: user.label,
                              value: user.value,
                              role: user.role,
                           })),
                        },
                     ]}
                     defaultLabel='Пользователь'
                     placeholder='Выберите пользователя'
                     svg={<User className='w-4' />}
                     onSelect={handleAddUser}
                  />
                  <div className='max-w-[380px] space-y-2'>
                     {selectedUsers.map((user, index) => (
                        <div key={index} className='flex items-center justify-between rounded bg-accent px-3 py-2'>
                           <p className='text-sm'>{user}</p>
                           <Button size='icon' variant='ghost' onClick={() => handleRemoveUser(user)}>
                              <X className='h-4 w-4' />
                           </Button>
                        </div>
                     ))}
                  </div>
               </div>
            </div>
         </CardContent>
         <CardFooter className='flex flex-wrap items-center justify-between border-t sm:h-32 lg:h-20'></CardFooter>
      </Card>
   );
};
