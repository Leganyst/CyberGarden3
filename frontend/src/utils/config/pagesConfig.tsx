import type { RouteObject } from 'react-router-dom';

import { MainPage } from '@/pages/MainPage/MainPage';
import { NotFoundPage } from '@/pages/NotFoundPage/NotFoundPage';
import { ProfilePage } from '@/pages/ProfilePage/ProfilePage';
import { ProjectPage } from '@/pages/ProjectPage/ProjectPage';
import { SchedulePage } from '@/pages/SchedulePage/SchedulePage';
import { Statistic } from '@/pages/Statistic/Statistic';

export enum AppRoutes {
   MAIN = 'main',
   PROFILE = 'profile',
   PROJECT = 'project',
   SCHEDULE = 'schedule',
   NOT_FOUND = 'not_found',
   STATISTIC = 'statistic',
}

export const RoutePath: Record<AppRoutes, string> = {
   [AppRoutes.MAIN]: '/',
   [AppRoutes.PROFILE]: '/profile',
   [AppRoutes.NOT_FOUND]: '*',
   [AppRoutes.PROJECT]: '/projects/:id', // Параметр id для страницы проекта
   [AppRoutes.SCHEDULE]: '/schedule',
   [AppRoutes.STATISTIC]: '/statistic',
};

export const routeConfig: Record<AppRoutes, RouteObject> = {
   [AppRoutes.MAIN]: {
      path: RoutePath.main,
      element: <MainPage />,
   },
   [AppRoutes.PROFILE]: {
      path: RoutePath.profile,
      element: <ProfilePage />,
   },

   [AppRoutes.PROJECT]: {
      path: RoutePath.project,
      element: <ProjectPage />, // Добавляем новую страницу
   },
   [AppRoutes.SCHEDULE]: {
      path: RoutePath.schedule,
      element: <SchedulePage />, // Добавляем новую страницу
   },
   [AppRoutes.NOT_FOUND]: {
      path: RoutePath.not_found,
      element: <NotFoundPage />,
   },
   [AppRoutes.STATISTIC]: {
      path: RoutePath.statistic,
      element: <Statistic />,
   },
};
