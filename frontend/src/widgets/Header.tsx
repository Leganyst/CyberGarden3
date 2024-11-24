import { Link } from 'react-router-dom';
import { Dialog } from '@radix-ui/react-dialog';

import { AuthModal } from '@/modules/Auth/ui/AuthModal';
import { Button } from '@/shared/ui/button';
import { DialogTrigger } from '@/shared/ui/dialog';
import { cn } from '@/utils/lib/utils';
import { Container } from '@/widgets/Container';
import { SeachInput } from '@/widgets/SeachInput';
import { ThemeSwitcher } from './ThemeSwitcher';
import { SidebarTrigger } from '@/shared/ui/sidebar';
import { useTokenStore } from '@/modules/Auth/model/store/authStore';

interface HeaderProps {
   className?: string;
}

export const Header = ({ className }: HeaderProps) => {
   const { accessToken } = useTokenStore();
   return (
      <header className={cn('h-[var(--header-height)]', className)}>
         <div className='flex h-full border border-l-0 border-border bg-background-secondary'>
            {accessToken && (
               <div className='flex items-center p-4'>
                  <SidebarTrigger className='-ml-1' />
               </div>
            )}

            <div className='flex h-full flex-1 bg-background-secondary'>
               <div className='flex flex-1 items-center justify-end py-5 pl-6 pr-7'>
                  <div className='flex items-center gap-2'>
                     <AuthModal />
                     <ThemeSwitcher />
                  </div>
               </div>
            </div>
         </div>
      </header>
   );
};
