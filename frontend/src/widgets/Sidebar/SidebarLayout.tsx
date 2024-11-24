import * as React from 'react';
import { Sidebar, SidebarContent, SidebarGroup, SidebarGroupContent, SidebarHeader, SidebarRail } from '@/shared/ui/sidebar';
import { Link } from 'react-router-dom';
import { Plus, X } from 'lucide-react';
import { SidebarProfile } from './SidebarItems/SidebarProfile';
import { SidebarPages } from './SidebarPages';
import { SidebarAccordeon } from './SidebarAccordeon';
import { CreateTaskModal } from '@/modules/Task/ui/CreateTaskModal';
import { Task } from '@/modules/Task/ui/Task';
import CenterInvestLogo from '@/shared/assets/СenterInvest.png';

export function SidebarLayout({ ...props }: React.ComponentProps<typeof Sidebar>) {
   return (
      <Sidebar {...props}>
         <SidebarHeader>
            <Link className='flex items-center gap-[10px] border-border px-3 py-2' to='/'>
               <div className='flex items-center gap-3 text-[20px]'>
                  <span>
                     <strong>bigas</strong> <span className='font-light'>production</span>
                  </span>
                  <span className='font-meduim text-2xl'>x</span>
                  <img alt='CenterInvest' className='mt-2 h-8 w-8' src={CenterInvestLogo} />
               </div>
            </Link>
         </SidebarHeader>
         <SidebarContent>
            <SidebarGroup>
               <SidebarProfile />
               <SidebarGroupContent>
                  <CreateTaskModal
                     buttonChildren='Добавить задачу'
                     buttonClassName='custom-button-class'
                     buttonIcon={<Plus className='rounded-full bg-primary text-background' size={24} />}
                     closeClassName='absolute right-2 top-2 rounded-sm'
                     closeIcon={<X className='h-4 w-4' />}
                     modalClassName='p-0'
                     overlayClassName='bg-black/15'
                  >
                     <Task />
                  </CreateTaskModal>
               </SidebarGroupContent>
               <SidebarGroupContent>
                  <SidebarPages />
               </SidebarGroupContent>
               <SidebarGroupContent>
                  <SidebarAccordeon />
               </SidebarGroupContent>
            </SidebarGroup>
         </SidebarContent>
         <SidebarRail />
      </Sidebar>
   );
}
