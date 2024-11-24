import { Task } from '@/modules/Task';
import { useTaskStore } from '@/modules/Task/model/store/TaskStore';
import { CreateTaskModal } from '@/modules/Task/ui/CreateTaskModal';
import { CheckboxTask } from '@/modules/Task/ui/checkBocks';
import { useFetchProjectById } from '@/modules/projects/api/GetProject';
import { useProjectStore } from '@/modules/projects/model/useProjectStore';
import { Button } from '@/shared/ui/button';
import { Loader } from '@/shared/ui/loader';
import { Container } from '@/widgets/Container';
import type { AxiosError } from 'axios';
import { Plus, X } from 'lucide-react';
import { useEffect } from 'react';
import { useParams } from 'react-router-dom';

export const ProjectPage = () => {
   const { id } = useParams<{ id: string }>();
   const { selectedProjectId, setSelectedProjectId, setCurrentProject } = useProjectStore();
   const { taskStates } = useTaskStore(); // Получаем состояние из Zustand

   useEffect(() => {
      const numericProjectId = Number(id);
      setSelectedProjectId(numericProjectId!);
   }, [id]);

   const { data: project, isLoading, isError, error } = useFetchProjectById(selectedProjectId!);

   useEffect(() => {
      if (!isLoading) {
         setCurrentProject(project!);
      }
   }, [project]);

   const isAnyTaskChecked = Object.values(taskStates).some((value) => value === true); // Проверяем, есть ли выбранные задачи
   if (isLoading) {
      return (
         <Container>
            <div className='flex h-screen w-full items-center justify-center'>
               <Loader className='h-16 w-16' />
            </div>
         </Container>
      );
   }

   if (isError) {
      return (
         <div>
            <p>Ошибка загрузки проекта:</p>
            <p>{(error as AxiosError).message}</p>
         </div>
      );
   }

   return (
      <Container>
         <div className='mt-14 flex flex-col gap-8'>
            <div className='flex justify-between'>
               <h1 className='text-4xl font-bold'>{project?.name}</h1>
               {isAnyTaskChecked && <Button className='bg-red-500 hover:bg-red-400'>Закрыть все задачи</Button>}
            </div>

            <div className='flex flex-col'>
               <div className='text-xl font-bold'>23 ноября · Сегодня · Суббота</div>
               <div>
                  <CheckboxTask />
               </div>
               <div className='hover:cursor-pointer'>
                  <span className='flex gap-2 text-gray-600'>
                     <CreateTaskModal
                        buttonChildren={
                           <div className='flex gap-2'>
                              <Plus className='text-primary' />
                              Добавить задачу
                           </div>
                        }
                        buttonClassName='custom-button-class'
                        closeClassName='absolute right-2 top-2 rounded-sm'
                        closeIcon={<X className='h-4 w-4' />}
                        modalClassName='p-0'
                        overlayClassName='bg-black/15'
                     >
                        <Task />
                     </CreateTaskModal>
                  </span>
               </div>
            </div>
         </div>
      </Container>
   );
};
