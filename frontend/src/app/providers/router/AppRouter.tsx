import { createBrowserRouter } from 'react-router-dom';

import BaseLayout from '@/app/layout/BaseLayout';
import { MainPage } from '@/pages/MainPage/MainPage';
import { routeConfig } from '@/utils/config/pagesConfig';

export const appRouter = createBrowserRouter(
   [
      {
         element: <BaseLayout />,
         // errorElement: <ErrorPage />,

         children: Object.values(routeConfig).map((route) => ({
            path: route.path,
            element: route.element,
         })),
      },
   ],
   {
      future: {
         v7_relativeSplatPath: true,
         v7_fetcherPersist: true,
         v7_normalizeFormMethod: true,
         v7_partialHydration: true,
         v7_skipActionErrorRevalidation: true,
      },
   },
);
