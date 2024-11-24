import { Calculator, CreditCard, Settings, Smile, User } from 'lucide-react';

import {
   Command,
   CommandEmpty,
   CommandGroup,
   CommandInput,
   CommandItem,
   CommandList,
   CommandSeparator,
   CommandShortcut,
} from '@/shared/ui/command';
import { Calendar } from '@/shared/ui/calendar';

export function CommandCalendar() {
   return (
      <Command className='rounded-lg border shadow-md md:min-w-[450px]'>
         <CommandInput placeholder='Type a command or search...' />
         <CommandList>
            <CommandEmpty>No results found.</CommandEmpty>
            <CommandGroup heading='Suggestions'>
               <Calendar />
            </CommandGroup>
            <CommandSeparator />
         </CommandList>
      </Command>
   );
}
