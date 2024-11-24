# Stage: Development
FROM node:18 AS dev
WORKDIR /app

# Установка pnpm глобально
RUN npm install -g pnpm

# Копируем только файлы зависимостей
COPY pnpm-lock.yaml ./ 
COPY package.json ./

# Удаление папки node_modules (если она существует в образе/кэше) для предотвращения конфликтов
RUN rm -rf node_modules

# Установка зависимостей с pnpm
RUN pnpm install

# Копируем остальные файлы проекта
COPY . .

# Удаляем node_modules из приложения, если они случайно скопировались
RUN rm -rf ./node_modules && pnpm install

# Открываем порт для dev-сервера
EXPOSE 3000

# Команда для запуска dev-режима
CMD ["pnpm", "dev"]
