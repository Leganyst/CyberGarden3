import { useSchedule } from '@/modules/Schedule/api/scheduleQuery';
import React, { useState } from 'react';

export const SchedulePage = () => {
   const [group, setGroup] = useState('');
   const [currentGroup, setCurrentGroup] = useState<string | null>(null);

   const { data: schedule, isLoading, isError, error } = useSchedule(currentGroup || '');

   const handleFetchSchedule = () => {
      if (group.trim()) {
         setCurrentGroup(group.trim());
      }
   };

   const renderSchedule = () => {
      if (!schedule || !schedule.table) return null;

      const { table } = schedule.table;

      return table.slice(2).map((daySchedule: string[], index: number) => {
         const [day, ...lessons] = daySchedule;

         return (
            <div key={index} className='mb-6 rounded-lg bg-white p-4 shadow-md'>
               <h2 className='text-lg font-semibold text-blue-600'>{day}</h2>
               <ul className='mt-2 space-y-2'>
                  {lessons.map((lesson, lessonIndex) =>
                     lesson ? (
                        <li key={lessonIndex} className='rounded-md border border-blue-300 bg-blue-50 p-3 shadow-sm'>
                           {lesson}
                        </li>
                     ) : (
                        <li key={lessonIndex} className='rounded-md border bg-gray-50 p-3 text-gray-500 shadow-sm'>
                           Нет занятий
                        </li>
                     ),
                  )}
               </ul>
            </div>
         );
      });
   };

   return (
      <div className='min-h-screen bg-gray-100 p-4 dark:bg-gray-900 sm:p-6'>
         <div className='mx-auto w-full max-w-2xl rounded-lg bg-white p-4 shadow-md dark:bg-gray-800 sm:max-w-3xl sm:p-6'>
            {/* Заголовок */}
            <h1 className='mb-4 text-center text-xl font-bold text-blue-700 dark:text-blue-300 sm:mb-6 sm:text-2xl'>
               Расписание занятий
            </h1>

            {/* Поле ввода и кнопка */}
            <div className='mb-4 flex flex-col gap-4 sm:flex-row'>
               <input
                  className='flex-1 rounded-lg border p-3 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 dark:border-gray-700 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 sm:text-base'
                  placeholder='Введите группу (например, КТбо2-8)'
                  type='text'
                  value={group}
                  onChange={(e) => setGroup(e.target.value)}
               />
               <button
                  className='rounded-lg bg-blue-500 px-4 py-3 text-sm font-medium text-white shadow transition hover:bg-blue-400 disabled:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600 sm:px-6 sm:py-3 sm:text-base'
                  disabled={isLoading}
                  onClick={handleFetchSchedule}
               >
                  {isLoading ? 'Загрузка...' : 'Получить расписание'}
               </button>
            </div>

            {/* Ошибка */}
            {isError && (
               <div className='rounded-md bg-red-100 p-4 text-sm text-red-600 shadow dark:bg-red-900 dark:text-red-400 sm:text-base'>
                  {(error as Error).message}
               </div>
            )}

            {/* Расписание */}
            {schedule && (
               <div className='mt-6'>
                  <h2 className='text-lg font-bold text-gray-700 dark:text-gray-300 sm:text-xl'>
                     {schedule.table.name} (Неделя {schedule.table.week})
                  </h2>
                  <div className='mt-4 overflow-x-auto'>{renderSchedule()}</div>
               </div>
            )}
         </div>
      </div>
   );
};
