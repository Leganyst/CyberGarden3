import { SidebarMenu, SidebarMenuButton, SidebarMenuItem } from '@/shared/ui/sidebar';
import { cn } from '@/utils/lib/utils';
import { Award, BookMarked, Calendar } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

const items = [
   {
      title: 'Сегодня',
      url: '/',
      icon: Calendar,
   },
   {
      title: 'Расписание вуза',
      url: '/schedule',
      icon: BookMarked,
   },
   {
      title: 'Достижения',
      url: '/achievements',
      icon: Award,
   },
];

export const SidebarPages = () => {
   const location = useLocation();

   return (
      <SidebarMenu>
         {items.map((item) => {
            const isActive = location.pathname === item.url; // Сравниваем текущий путь с URL элемента
            return (
               <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton
                     asChild
                     className={cn('px-2.5', {
                        'bg-accent': isActive, // Активный стиль
                     })}
                  >
                     <Link to={item.url}>
                        <item.icon size={16} />
                        <span>{item.title}</span>
                     </Link>
                  </SidebarMenuButton>
               </SidebarMenuItem>
            );
         })}
      </SidebarMenu>
   );
};
