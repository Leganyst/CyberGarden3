import React from 'react';
import clsx from 'clsx';

type TitleSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
type TagType = 'h5' | 'h4' | 'h3' | 'h2' | 'h1' | 'p';

interface TitleProps {
   tag?: TagType;
   size?: TitleSize;
   className?: string;
   text: string;
}

export const Title = ({ tag = 'p', text, size = 'sm', className }: TitleProps) => {
   // Парметры в зависимости от пропсов
   const mapTagBySize = {
      h5: 'h5',
      h4: 'h4',
      h3: 'h3',
      h2: 'h2',
      h1: 'h1',
      // "2xl": "h1",
      p: 'p',
   } as const; //const = только для чтения

   const mapClassNameBySize = {
      xs: 'text-[12px]',
      sm: 'text-[14px]',
      md: 'text-[16px]',
      lg: 'text-[20px]',
      xl: 'text-[24px]',
      '2xl': 'text-[32px]',
   } as const;

   const Comp = mapTagBySize[tag];

   return <Comp className={clsx(mapClassNameBySize[size], className)}>{text}</Comp>;
};
