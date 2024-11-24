import { Button } from '@/shared/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuTrigger } from '@/shared/ui/dropdown-menu';
import { cn } from '@/utils/lib/utils';
import type { ReactNode } from 'react';

interface TaskCommandProps {
   btnWidth?: string;
   children: ReactNode;
   className?: string;
   slot?: boolean;
   svg?: ReactNode;
   text: string;
   rounded?: boolean;
}

export function TaskCommand({ svg, text, children, className, slot, btnWidth, rounded }: TaskCommandProps) {
   return (
      <DropdownMenu>
         <DropdownMenuTrigger asChild className={className}>
            <Button className={cn('h-8 min-w-[120px] justify-between gap-2', btnWidth)} variant='outline'>
               {rounded ? <div className={`h-3 w-3 rounded-full ${svg}`}></div> : svg}

               {text}
               {slot && <span className='h-6 w-6' />}
            </Button>
         </DropdownMenuTrigger>
         <DropdownMenuContent className='border-none'>{children}</DropdownMenuContent>
      </DropdownMenu>
   );
}
