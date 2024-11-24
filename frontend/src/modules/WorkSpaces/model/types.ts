// Тип для групп пользователей
interface Group {
   id: number;
   name: string;
}

// Тип для пользователей (спикеров, менеджеров, участников)
interface User {
   id: number;
   username: string;
   first_name: string;
   last_name: string;
   avatar: string;
   job: string;
   vk: string | null;
   telegram: string | null;
   mail: string | null;
   phone_number: string | null;
   groups: Group[];
   score: number;
}

// Тип для продолжительности события
interface Duration {
   hours: number;
   minutes: number;
   seconds: number;
}

// Тип для категории события
interface EventType {
   id: number;
   name: string;
}

// Основной тип для события
export interface Event {
   id: number;
   name: string;
   place: string;
   time_start: string; // Формат ISO 8601, можно использовать тип Date при необходимости
   time_end: string; // Формат ISO 8601, можно использовать тип Date при необходимости
   duration: Duration;
   is_upcoming: boolean;
   user_state: any | null; // Необходимо уточнить структуру, если известна
   reference: string | null;
   reference_video: string | null;
   type: EventType;
   speaker: User | null;
   managers: User[];
   participants: User[];
   image: string; // URL изображения
   is_online: boolean;
   description: string;
}

// Пример использования: массив событий
export interface Events {
   Events: Event[];
}
