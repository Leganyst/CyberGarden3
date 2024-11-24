import { useEffect, useState } from 'react';
import { Button } from '@/shared/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTrigger } from '@/shared/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/shared/ui/tabs';
import { RegistrationForm } from './RegistrationForm';
import { LoginForm } from './LoginForm';
import { useTokenStore } from '../model/store/authStore';
import { cn } from '@/utils/lib/utils';
import TelegramLoginButton from './telegrammBtn';

interface AuthModalProps {
   authModalMode?: 'login' | 'register';
   className?: string;
}

export function AuthModal({ className, authModalMode = 'login' }: AuthModalProps) {
   const [isLoading, setisLoading] = useState(false);
   const [open, setOpen] = useState(false);
   const { accessToken, clearAccessToken, clearRefreshToken } = useTokenStore();

   const toggleOpenStatus = (status: boolean) => {
      setOpen(status);
   };

   const clearStorage = () => {
      clearAccessToken();
      clearRefreshToken();
      setOpen(false);
   };

   const setLoadingStatus = (status: boolean) => {
      setisLoading(status);
   };

   return (
      <>
         {accessToken ? (
            <Button className='flex gap-2' size='small' variant='secondary' onClick={clearStorage}>
               Выйти
            </Button>
         ) : (
            <Dialog open={open} onOpenChange={setOpen}>
               <DialogTrigger asChild>
                  <Button className={cn(className, 'flex gap-2')} size='small' variant='secondary'>
                     {authModalMode === 'login' && 'Вход'}
                     {authModalMode === 'register' && 'Регистрация'}
                  </Button>
               </DialogTrigger>
               <Tabs defaultValue={authModalMode}>
                  <DialogContent aria-describedby='dialog-description' className='flex flex-col sm:max-w-md'>
                     <DialogHeader className='h-6'>
                        {!isLoading && (
                           <TabsList>
                              <TabsTrigger className='hover:bg-background' value='login'>
                                 Авторизация
                              </TabsTrigger>
                              <TabsTrigger className='hover:bg-background' value='register'>
                                 Регистрация
                              </TabsTrigger>
                           </TabsList>
                        )}
                     </DialogHeader>
                     <TabsContent value='login'>
                        <LoginForm setLoadingStatus={setLoadingStatus} toggleOpenStatus={toggleOpenStatus} />
                        {/* <TelegramLoginButton
                           botName='bigas_notification_bot' // Имя вашего бота
                           buttonSize='large' // Размер кнопки
                           className='h-4 bg-blue-400'
                           cornerRadius={3} // Радиус скругления
                           dataAuthUrl='https://cybergarden.leganyst.ru/auth/telegram' // Укажите ваш реальный домен здесь
                           usePic={false} // Показывать ли фото пользователя
                        /> */}
                     </TabsContent>
                     <TabsContent value='register'>
                        <RegistrationForm setLoadingStatus={setLoadingStatus} toggleOpenStatus={toggleOpenStatus} />
                     </TabsContent>
                  </DialogContent>
               </Tabs>
            </Dialog>
         )}
      </>
   );
}
