import { useTheme } from '@/app/providers/theme/ThemeProvider';
import { Button } from '@/shared/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/shared/ui/dropdown-menu';
import { Moon, Sun } from 'lucide-react';

export function ThemeSwitcher({ className }: { className?: string }) {
   const { setTheme } = useTheme();

   return (
      <DropdownMenu>
         <DropdownMenuTrigger asChild className={className}>
            <Button size='icon' variant='secondary'>
               <Sun className='h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0' />
               <Moon className='absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100' />
               <span className='sr-only'>Переключить тему</span>
            </Button>
         </DropdownMenuTrigger>
         <DropdownMenuContent align='end'>
            <DropdownMenuItem onClick={() => setTheme('light')}>Светлая</DropdownMenuItem>
            <DropdownMenuItem onClick={() => setTheme('dark')}>Тёмная</DropdownMenuItem>
            <DropdownMenuItem onClick={() => setTheme('system')}>Системная</DropdownMenuItem>
         </DropdownMenuContent>
      </DropdownMenu>
   );
}
