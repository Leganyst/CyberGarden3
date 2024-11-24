import * as React from 'react';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';
import { cn } from '@/utils/lib/utils';
import { Popover, PopoverContent, PopoverTrigger } from '@/shared/ui/popover';
import { Button } from '@/shared/ui/button';
import { Calendar } from '@/shared/ui/calendar';

interface DatePickerProps {
   className?: string;
   pickerName: string;
   svg?: React.ReactNode;
   selectedDate?: Date;
   onDateChange?: (date: Date | undefined) => void;
}

export function DatePicker({ pickerName, svg, className, selectedDate, onDateChange }: DatePickerProps) {
   return (
      <Popover>
         <PopoverTrigger asChild>
            <Button
               className={cn(
                  'flex h-8 min-w-[200px] justify-start gap-2 text-left font-normal',
                  !selectedDate && 'text-muted-foreground',
                  className,
               )}
               variant={'outline'}
            >
               {svg}
               {selectedDate ? format(selectedDate, 'PPP', { locale: ru }) : <span>{pickerName}</span>}
            </Button>
         </PopoverTrigger>
         <PopoverContent align='start' className='w-auto p-0'>
            <Calendar initialFocus mode='single' selected={selectedDate} onSelect={onDateChange} />
         </PopoverContent>
      </Popover>
   );
}
