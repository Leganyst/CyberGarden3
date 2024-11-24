import { z } from 'zod';
import { loginSchema } from './LoginForm';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRegister } from '../model/api/RegisterApi';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/shared/ui/form';
import { Input } from '@/shared/ui/input';
import { Button } from '@/shared/ui/button';
import { Title } from '@/shared/ui/title';
import { useEffect, useState } from 'react';
import { useTokenStore } from '../model/store/authStore';
import { Loader } from '@/shared/ui/loader';
import { useCreateWorkspace } from '@/modules/WorkSpaces/model/api/workSpacesPost';
import { useWorkspaceStore } from '@/modules/WorkSpaces/model/store/workSpaceStore';
import { useLogin } from '../model/api/LoginApi';
import { useNavigate } from 'react-router-dom';

const registerSchema = loginSchema
   .extend({
      name: z.string().min(3, { message: 'Имя пользователя должно быть не менее 3 символов' }),
      confirmPassword: z.string().min(2, { message: 'Пароль должен быть не менее 8 символов' }),
   })
   .refine((data) => data.password === data.confirmPassword, {
      message: 'Пароли должны совпадать',
      path: ['confirmPassword'],
   });

interface RegistrationFormProps {
   setLoadingStatus: (status: boolean) => void;
   toggleOpenStatus: (status: boolean) => void;
}

export const RegistrationForm = ({ toggleOpenStatus, setLoadingStatus }: RegistrationFormProps) => {
   const { mutateAsync: register, isPending: isRegistering } = useRegister();
   const { mutateAsync: login, isPending: isLoggingIn } = useLogin();
   const { mutateAsync: createWorkspace } = useCreateWorkspace();
   const { setAccessToken, setRefreshToken } = useTokenStore();
   const addWorkspace = useWorkspaceStore((state) => state.addWorkspace);
   const navigate = useNavigate(); // Навигация
   const [error, setError] = useState<string | null>(null);

   useEffect(() => {
      setLoadingStatus(isRegistering || isLoggingIn); // Учитываем состояние загрузки регистрации и логина
   }, [isRegistering, isLoggingIn]);

   const registerForm = useForm<z.infer<typeof registerSchema>>({
      resolver: zodResolver(registerSchema),
      defaultValues: {
         email: '',
         password: '',
         name: '',
         confirmPassword: '',
      },
   });

   const onSubmit = async (values: z.infer<typeof registerSchema>) => {
      setError(null);
      try {
         // Регистрация
         const registerData = await register(values);
         setAccessToken(registerData.access_token);
         setRefreshToken(registerData.refresh_token);

         // Автоматический логин
         const loginData = await login({ email: values.email, password: values.password });
         setAccessToken(loginData.access_token);
         setRefreshToken(loginData.refresh_token);

         // Создание воркспейса
         const workspace = await createWorkspace({ name: 'newSpace', created_by: loginData.user_id });
         addWorkspace(workspace);

         toggleOpenStatus(false); // Закрываем форму
         navigate('/'); // Перенаправляем на главную страницу
      } catch (err) {
         console.error('Ошибка в процессе регистрации:', err);
         setError('Ошибка при регистрации. Попробуйте ещё раз.');
      }
   };

   return (
      <>
         {isRegistering || isLoggingIn ? (
            <div className='flex h-60 w-full items-center justify-center'>
               <Loader />
            </div>
         ) : (
            <Form {...registerForm}>
               <form className='space-y-4' onSubmit={registerForm.handleSubmit(onSubmit)}>
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
                     control={registerForm.control}
                     name='email'
                  />
                  <FormField
                     render={({ field }) => (
                        <FormItem>
                           <FormLabel>Имя пользователя</FormLabel>
                           <FormControl>
                              <Input placeholder='Введите имя пользователя' type='text' {...field} />
                           </FormControl>
                           <FormMessage />
                        </FormItem>
                     )}
                     control={registerForm.control}
                     name='name'
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
                     control={registerForm.control}
                     name='password'
                  />
                  <FormField
                     render={({ field }) => (
                        <FormItem>
                           <FormLabel>Подтвердите пароль</FormLabel>
                           <FormControl>
                              <Input placeholder='Повторите пароль' type='password' {...field} />
                           </FormControl>
                           <FormMessage />
                        </FormItem>
                     )}
                     control={registerForm.control}
                     name='confirmPassword'
                  />
                  {error && <Title className='text-red-500' text={error} />}
                  <Button className='w-[160px]' type='submit'>
                     Зарегистрироваться
                  </Button>
               </form>
            </Form>
         )}
      </>
   );
};
