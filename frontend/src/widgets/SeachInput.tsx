import { useState } from 'react';
import { useClickOutside } from '@siberiacancode/reactuse';

import { cn } from '@/utils/lib/utils';
import { Input } from '@/shared/ui/input';

interface SeachInputProps {
   className?: string;
}

export const SeachInput = ({ className }: SeachInputProps) => {
   const [focused, setFocused] = useState(false);

   const clickOutsideRef = useClickOutside<HTMLDivElement>(() => {
      setFocused(false);
   });

   return (
      <div ref={clickOutsideRef} className={cn('')}>
         <label htmlFor='search-input'>{/* <Icon20Search /> */}</label>
         <Input
            className={'h-8 rounded-md border bg-secondary py-[1px] pl-[8px] pr-[6px]'}
            placeholder='Поиск товаров'
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            id='search-input'
         />
      </div>
   );
};
