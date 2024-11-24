import { Outlet } from 'react-router-dom';

import { Footer } from '@/widgets/Footer';
import { Header } from '@/widgets/Header';
import { SidebarInset, SidebarProvider } from '@/shared/ui/sidebar';
import { Sidebar } from '@/widgets';
import { useTokenStore } from '@/modules/Auth/model/store/authStore';
import { ThemeSwitcher } from '@/widgets/ThemeSwitcher';
import { AuthModal } from '@/modules/Auth/ui/AuthModal';
import NonAuthImage from '@/shared/assets/NonAuthImage.png';

const BaseLayout = () => {
   const { accessToken } = useTokenStore();

   return (
      <>
         {accessToken ? (
            <SidebarProvider>
               <Sidebar />
               <SidebarInset>
                  <div className='h-screen bg-background'>
                     <Header />
                     <div className='px-6'>
                        <Outlet />
                     </div>
                     <Footer />
                  </div>
               </SidebarInset>
            </SidebarProvider>
         ) : (
            <div className='relative flex h-screen items-center justify-center gap-3 bg-background px-4 sm:px-6 lg:px-8'>
               <ThemeSwitcher className='absolute right-4 top-4' />
               <img
                  alt='Изображение для стартовой страницы'
                  className='hidden h-[800px] w-[800px] md:h-[500px] md:w-[500px] lg:block lg:h-[600px]'
                  src={NonAuthImage}
               />
               <div className='flex max-w-[700px] flex-col gap-8 text-center lg:gap-16'>
                  <p className='text-xl font-bold md:text-2xl lg:text-3xl'>
                     Присоединяйся к тем, кто уже живет с удовольствием, управляй задачами, анализируй нагрузку и наслаждайся
                     успехом!
                  </p>
                  <div className='flex flex-col items-center gap-3 md:flex-row'>
                     <AuthModal className='h-12 w-48 bg-primary text-base font-bold uppercase hover:bg-primary-hover md:h-[56px] md:w-56 md:text-xl' />
                     <AuthModal
                        authModalMode='register'
                        className='h-12 w-48 border border-primary text-base font-bold uppercase md:h-[56px] md:w-56 md:text-xl'
                     />
                  </div>
               </div>
            </div>
         )}
      </>
   );
};

export default BaseLayout;
