import { Plus, X } from 'lucide-react';
import { Button } from '@/shared/ui/button';
import { CheckboxTask } from './checkBocks';
import { useTaskStore } from '../model/store/TaskStore';
import { CreateTaskModal } from './CreateTaskModal';
import { Task } from './Task';

interface TaskProps {
   className?: string;
}

export const TaskPage = ({ className }: TaskProps) => {
   const { taskStates } = useTaskStore(); // Получаем состояние из Zustand
   const isAnyTaskChecked = Object.values(taskStates).some((value) => value === true); // Проверяем, есть ли выбранные задачи

   return (
      <div className='mt-14 flex flex-col gap-8'>
         <div className='flex justify-between'>
            <h1 className='text-4xl font-bold'>Сегодня</h1>
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
   );
};
