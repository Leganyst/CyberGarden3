import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { useLogin } from '../model/api/LoginApi';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/shared/ui/form';
import { Input } from '@/shared/ui/input';
import { useEffect, useState } from 'react';
import { Button } from '@/shared/ui/button';
import { Title } from '@/shared/ui/title';
import { useTokenStore } from '../model/store/authStore';
import { Loader } from '@/shared/ui/loader';
import TelegramLoginButton from './telegrammBtn';
import { useFetchWorkspacesAsync } from '@/modules/WorkSpaces/model/api/workSpacesGet';
import { useNavigate } from 'react-router-dom';

export const loginSchema = z.object({
   email: z.string().email({ message: 'Некорректный email' }),
   password: z.string().min(8, { message: 'Пароль должен быть не менее 8 символов' }),
});

interface LoginFormProps {
   setLoadingStatus: (status: boolean) => void;
   toggleOpenStatus: (status: boolean) => void;
}

export const LoginForm = ({ toggleOpenStatus, setLoadingStatus }: LoginFormProps) => {
   const { setAccessToken, setRefreshToken } = useTokenStore();
   const { refetch: fetchWorkspaces, isFetching } = useFetchWorkspacesAsync();
   const { mutateAsync: login, isPending } = useLogin();
   const [error, setError] = useState<string | null>(null);
   const navigate = useNavigate(); // Инициализация навигации

   useEffect(() => {
      setLoadingStatus(isPending || isFetching); // Учитываем загрузку логина и рабочих пространств
   }, [isPending, isFetching]);

   const loginForm = useForm<z.infer<typeof loginSchema>>({
      resolver: zodResolver(loginSchema),
      defaultValues: {
         email: '',
         password: '',
      },
   });

   const onLoginSubmit = async (values: z.infer<typeof loginSchema>) => {
      setError(null); // Сбрасываем предыдущую ошибку
      try {
         const data = await login(values); // Выполняем запрос на логин
         setAccessToken(data.access_token); // Сохраняем токены в Zustand
         setRefreshToken(data.refresh_token);

         // Выполняем запрос рабочих пространств после успешной авторизации
         await fetchWorkspaces();

         toggleOpenStatus(false); // Закрываем форму
         navigate('/');
      } catch (err) {
         console.error('Ошибка при входе:', err);
         setError('Ошибка при входе'); // Устанавливаем сообщение об ошибке
      }
   };

   return (
      <>
         {isPending || isFetching ? (
            <div className='flex h-60 w-full items-center justify-center'>
               <Loader />
            </div>
         ) : (
            <Form {...loginForm}>
               <form className='space-y-4' onSubmit={loginForm.handleSubmit(onLoginSubmit)}>
                  <FormField
                     render={({ field }) => (
                        <FormItem>
                           <FormLabel>Email</FormLabel>
                           <FormControl>
                              <Input placeholder='Введите email' {...field} />
                           </FormControl>
                           <FormMessage />
                        </FormItem>
                     )}
                     control={loginForm.control}
                     name='email'
                  />

                  <FormField
                     render={({ field }) => (
                        <FormItem>
                           <FormLabel>Пароль</FormLabel>
                           <FormControl>
                              <Input placeholder='Введите пароль' type='password' {...field} />
                           </FormControl>
                           <FormMessage />
                        </FormItem>
                     )}
                     control={loginForm.control}
                     name='password'
                  />
                  {error && <Title className='text-red-500' text={error} />}
                  <Button className='w-[160px]' type='submit'>
                     Войти
                  </Button>
               </form>
            </Form>
         )}
      </>
   );
};
