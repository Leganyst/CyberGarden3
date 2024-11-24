import { cn } from '@/utils/lib/utils';
import * as React from 'react';

const Textarea = React.forwardRef<HTMLTextAreaElement, React.ComponentProps<'textarea'>>(({ className, ...props }, ref) => {
   const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      const textarea = e.target;

      textarea.style.height = `${textarea.scrollHeight}px`;
   };

   return (
      <textarea
         className={cn(
            'flex min-h-[40px] w-full rounded-md border border-input bg-transparent px-3 py-2 shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50',
            className,
         )}
         onInput={handleInput}
         ref={ref}
         {...props}
      />
   );
});

Textarea.displayName = 'Textarea';

export { Textarea };
