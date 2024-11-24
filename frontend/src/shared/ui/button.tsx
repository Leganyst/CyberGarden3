import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';

import { cn } from '@/utils/lib/utils';

const buttonVariants = cva(
   'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
   {
      variants: {
         variant: {
            default: 'bg-primary hover:bg-primary-hover text-primary-foreground shadow',
            secondary: 'bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary-hover border border-border',
            destructive: 'bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90',
            outline: 'border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground',
            ghost: 'hover:bg-accent hover:text-accent-foreground',
            link: 'text-primary underline-offset-4 hover:underline',
         },
         size: {
            default: 'h-10 px-[10px]',
            small: 'h-8 rounded-md px-1.5',
            large: 'h-12 rounded-md px-3.5',
            icon: 'h-8 w-8 rounded-md',
         },
      },
      defaultVariants: {
         variant: 'default',
         size: 'default',
      },
   },
);

export interface ButtonProps
   extends Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'prefix'>,
      VariantProps<typeof buttonVariants> {
   asChild?: boolean;
   children?: React.ReactNode;
   prefix?: React.ReactNode;
   suffix?: React.ReactNode;
   text?: string;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
   ({ className, children, text, variant, size, prefix, suffix, asChild = false, ...props }, ref) => {
      const Comp = asChild ? Slot : 'button';
      return (
         <Comp ref={ref} className={cn(buttonVariants({ variant, size, className }))} {...props}>
            {prefix && <span className='mr-2'>{prefix}</span>}
            {children || <span className='px-1.5'>{text}</span>}
            {suffix && <span className='ml-2'>{suffix}</span>}
         </Comp>
      );
   },
);
Button.displayName = 'Button';

export { Button, buttonVariants };
