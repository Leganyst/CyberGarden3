import { TaskComboBox } from '@/modules/Task/ui/TaskComboBox';
import { Button } from '@/shared/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuSeparator } from '@/shared/ui/dropdown-menu';
import { Input } from '@/shared/ui/input';
import { DropdownMenuTrigger } from '@radix-ui/react-dropdown-menu';
import { Plus, User, X } from 'lucide-react';
import { useState } from 'react';

import { useWorkspaceStore } from '@/modules/WorkSpaces/model/store/workSpaceStore';
import type { AxiosError } from 'axios';
import { useCreateProject } from '@/modules/projects/api/CreateProjectApi';
import { Loader } from '@/shared/ui/loader';

const usersData = [
   { label: 'Вилков В. В. (240303vilkov@gmail.com)', value: 'Вилков В. В. (240303vilkov@gmail.com)', role: 'Пользователь' },
   { label: 'Козлов А. А. (kozlov@example.com)', value: 'Козлов А. А. (kozlov@example.com)', role: 'Администратор' },
   { label: 'Семенова И. И. (semenova@example.com)', value: 'Семенова И. И. (semenova@example.com)', role: 'Менеджер' },
];

export const SidebarAddProject = () => {
   const isMobile = window.innerWidth <= 640;
   const [projectName, setProjectName] = useState('');
   const [selectedUsers, setSelectedUsers] = useState<string[]>([]);
   const [isDropdownOpen, setDropdownOpen] = useState(false);

   const currentWorkspaceId = useWorkspaceStore((state) => state.workspaces[0]?.id); // Получаем ID текущего рабочего пространства
   const { mutate: project, isPending } = useCreateProject(); // Подключаем хук для мутации

   const handleAddUser = (user: string) => {
      if (!selectedUsers.includes(user)) {
         setSelectedUsers((prev) => [...prev, user]);
      }
   };

   const handleRemoveUser = (user: string) => {
      setSelectedUsers((prev) => prev.filter((u) => u !== user));
   };

   const handleCreateProject = async () => {
      if (projectName.trim() && currentWorkspaceId) {
         project(
            {
               name: projectName,
               workspace_id: currentWorkspaceId,
               created_by: 1, // Здесь должен быть ID текущего пользователя, заменить на реальный
            },
            {
               onSuccess: () => {
                  setProjectName('');
                  setSelectedUsers([]);
                  setDropdownOpen(false);
               },
               onError: (error: AxiosError) => {
                  console.error('Ошибка при добавлении проекта:', error.message);
               },
            },
         );
      }
   };

   return (
      <DropdownMenu open={isDropdownOpen} onOpenChange={setDropdownOpen}>
         <DropdownMenuTrigger asChild>
            <Button className='h-5 w-5' disabled={isPending} size='icon' variant='ghost' onClick={(e) => e.stopPropagation()}>
               <Plus className='h-5 w-5' />
            </Button>
         </DropdownMenuTrigger>
         <DropdownMenuContent
            style={{
               transform: isMobile ? 'translateX(150px)' : 'none', // Сдвиг только на мобильных
            }}
            align='start'
            className='w-80 rounded-lg bg-white p-4 shadow-lg sm:w-96'
            side='right'
            sideOffset={24}
            onClick={(e) => e.stopPropagation()}
         >
            <div className='relative mb-4 flex items-center justify-between'>
               <h3 className='text-lg font-semibold'>Добавить проект</h3>
               {isPending && <Loader className='absolute right-8 top-0' />}
               <Button className='h-5 w-5' size='icon' variant='ghost' onClick={() => setDropdownOpen(false)}>
                  <X className='h-5 w-5' />
               </Button>
            </div>
            <DropdownMenuSeparator />
            <div className='space-y-4'>
               {/* Поле ввода имени проекта */}
               <div>
                  <label className='mb-1 block text-sm font-medium' htmlFor='projectName'>
                     Имя проекта
                  </label>
                  <Input
                     required
                     id='projectName'
                     placeholder='Введите имя проекта'
                     value={projectName}
                     onChange={(e) => setProjectName(e.target.value)}
                  />
               </div>

               {/* Выпадающий список для добавления пользователей */}
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

               {/* Кнопки действия */}
               <div className='flex justify-end gap-2'>
                  <Button variant='ghost' onClick={() => setDropdownOpen(false)}>
                     Отмена
                  </Button>
                  <Button disabled={!projectName.trim() || isPending} variant='default' onClick={handleCreateProject}>
                     {isPending ? 'Добавление...' : 'Добавить'}
                  </Button>
               </div>
            </div>
         </DropdownMenuContent>
      </DropdownMenu>
   );
};
