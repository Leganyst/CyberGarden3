import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';

import { appRouter } from './app/providers/router/AppRouter.tsx';
import { queryClient } from './shared/api/query-client.ts';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

import '@/app/styles/index.css';
import { ThemeProvider } from './app/providers/theme/ThemeProvider.tsx';

createRoot(document.getElementById('root')!).render(
   <ThemeProvider defaultTheme='dark' storageKey='vite-ui-theme'>
      <QueryClientProvider client={queryClient}>
         <RouterProvider
            future={{
               v7_startTransition: true,
            }}
            router={appRouter}
         />
         <ReactQueryDevtools initialIsOpen={false} />
      </QueryClientProvider>
   </ThemeProvider>,
);
