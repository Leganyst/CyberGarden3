import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/shared/ui/accordion';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem } from '@/shared/ui/dropdown-menu';
import { DropdownMenuTrigger } from '@radix-ui/react-dropdown-menu';
import { CheckIcon, EllipsisIcon, LayoutGrid, Plus, User, X } from 'lucide-react';
import { SidebarAddProject } from './SidebarAddProject';

import { useFetchProjectsByWorkspace } from '@/modules/projects/api/GetUserProjectsApi';
import { useDeleteProject } from '@/modules/projects/api/DeleteProjectApi';
import { Skeleton } from '@/shared/ui/skeleton';
import { useUpdateProject } from '@/modules/projects/api/UpdateProjectApi';
import { useState } from 'react';
import { Button } from '@/shared/ui/button';
import { useNavigate, useParams } from 'react-router-dom';
import { cn } from '@/utils/lib/utils';
import { Input } from '@/shared/ui/input';

// const projectItems = [
//    { label: 'Хакатон 🤯', value: 'Учёба' },
//    { label: 'Школа 👻', value: 'Рутины' },
//    { label: 'Домашние заботы 🧸', value: 'Вдохновение' },
// ];

export const SidebarAccordeon = () => {
   const { data: projects, isSuccess, isLoading: isProjectsLoading } = useFetchProjectsByWorkspace();
   const deleteProjectMutation = useDeleteProject();
   const updateProjectMutation = useUpdateProject();
   const [editingProjectId, setEditingProjectId] = useState<number | null>(null);
   const [newName, setNewName] = useState<string>('');
   const navigate = useNavigate();

   const { id: currentProjectId } = useParams<{ id: string }>(); // Извлечение ID из URL

   const startEditing = (id: number, currentName: string) => {
      setEditingProjectId(id);
      setNewName(currentName);
   };

   const saveEditing = () => {
      if (!editingProjectId) return;
      updateProjectMutation.mutate({ id: editingProjectId, name: newName });
      setEditingProjectId(null); // Сбрасываем состояние редактирования
   };

   const handleRedirect = (itemId: number) => {
      navigate(`/projects/${itemId}`);
   };

   return (
      <Accordion collapsible type='single'>
         <AccordionItem className='border-none' value='item-1'>
            <AccordionTrigger className='px-2.5 py-2'>
               <div className='mr-1 flex flex-1 justify-between'>
                  <div className='flex items-center gap-2 font-normal'>
                     <LayoutGrid size={16} />
                     Проекты
                  </div>
                  <SidebarAddProject />
               </div>
            </AccordionTrigger>
            <AccordionContent className='px-2.5 py-2'>
               {/* Скелетоны */}
               {isProjectsLoading && (
                  <div className='flex w-full flex-col gap-[2px]'>
                     {Array.from({ length: 8 }, (_, index) => (
                        <Skeleton key={index} className='h-8 w-full' />
                     ))}
                  </div>
               )}
               {/* Отображение проектов */}
               {isSuccess &&
                  projects.map((item) => (
                     <div
                        key={item.id}
                        className={cn(
                           'group/item relative flex cursor-pointer justify-between rounded-[4px] bg-sidebar px-2 py-1.5 hover:bg-sidebar-accent',
                           {
                              'bg-accent font-semibold': currentProjectId === String(item.id), // Подсветка активного проекта
                           },
                        )}
                        onClick={() => handleRedirect(item.id)}
                     >
                        {editingProjectId === item.id ? (
                           <div className='flex items-center gap-2'>
                              <Input value={newName} onChange={(e) => setNewName(e.target.value)} />
                              <Button className='absolute right-2 h-6 w-6' size='icon' onClick={saveEditing}>
                                 <CheckIcon size={20} />
                              </Button>
                           </div>
                        ) : (
                           <p className='peer'>{item.name}</p>
                        )}

                        <DropdownMenu>
                           <DropdownMenuTrigger
                              asChild
                              className='invisible rounded-[4px] bg-sidebar-accent transition-opacity duration-200 hover:bg-sidebar group-hover/item:visible data-[state=open]:visible data-[state=open]:bg-accent'
                           >
                              <EllipsisIcon />
                           </DropdownMenuTrigger>
                           <DropdownMenuContent align='start' side='right'>
                              <DropdownMenuItem className='cursor-pointer'>
                                 <span onClick={() => startEditing(item.id, item.name)}>Изменить</span>
                              </DropdownMenuItem>
                              <DropdownMenuItem className='cursor-pointer'>
                                 <span className='text-red-500' onClick={() => deleteProjectMutation.mutate(item.id)}>
                                    Удалить
                                 </span>
                              </DropdownMenuItem>
                           </DropdownMenuContent>
                        </DropdownMenu>
                     </div>
                  ))}
            </AccordionContent>
         </AccordionItem>
      </Accordion>
   );
};
