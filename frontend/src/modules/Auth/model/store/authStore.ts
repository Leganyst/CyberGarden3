import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';

interface TokenState {
   accessToken: string | null;
   refreshToken: string | null;
   clearAccessToken: () => void;
   clearRefreshToken: () => void;
   setAccessToken: (token: string | null) => void;
   setRefreshToken: (token: string | null) => void;
}

export const useTokenStore = create(
   persist<TokenState>(
      (set) => ({
         accessToken: null,
         refreshToken: null,
         setAccessToken: (token: string | null) => {
            set({ accessToken: token });
         },
         setRefreshToken: (token: string | null) => {
            set({ refreshToken: token });
         },
         clearAccessToken: () => {
            set({ accessToken: null });
         },
         clearRefreshToken: () => {
            set({ refreshToken: null });
         },
      }),
      {
         name: 'token-storage',
         storage: createJSONStorage(() => localStorage),
      },
   ),
);
