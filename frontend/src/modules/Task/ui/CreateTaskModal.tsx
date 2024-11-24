import { Dialog, DialogOverlay, DialogPortal, DialogTrigger } from '@/shared/ui/dialog';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { cn } from '@/utils/lib/utils';
import { X } from 'lucide-react';
import React, { useState } from 'react';
import { Button } from '@/shared/ui/button';

interface CreateModalProps {
   buttonChildren?: string | React.ReactNode;
   buttonClassName?: string;
   buttonIcon?: React.ReactNode;
   children: React.ReactNode;
   closeClassName?: string;
   closeIcon?: React.ReactNode;
   modalClassName?: string;
   overlayClassName?: string;
   showButton?: boolean;
}

export const CreateModalContent = React.forwardRef<
   React.ElementRef<typeof DialogPrimitive.Content>,
   React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content> & {
      closeIcon?: React.ReactNode;
      closeClassName?: string;
      overlayClassName?: string;
   }
>(({ className, children, closeIcon, closeClassName, overlayClassName, ...props }, ref) => (
   <DialogPortal>
      <DialogOverlay className={cn('bg-black/15', overlayClassName)} />
      <DialogPrimitive.Content
         ref={ref}
         className={cn(
            'fixed left-[50%] top-[50%] z-50 grid w-full max-w-[1300px] translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg',
            className,
         )}
         {...props}
      >
         {children}
         <DialogPrimitive.Close
            className={cn(
               'absolute right-2 top-2 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none',
               closeClassName,
            )}
         >
            {closeIcon || <X className='h-4 w-4' />}
            <span className='sr-only'>Close</span>
         </DialogPrimitive.Close>
      </DialogPrimitive.Content>
   </DialogPortal>
));
CreateModalContent.displayName = 'CreateModalContent';

export const CreateTaskModal: React.FC<CreateModalProps> = ({
   children,
   buttonChildren = 'Добавить задачу',
   showButton = true,
   buttonIcon,
   buttonClassName,
   modalClassName,
   overlayClassName,
   closeIcon,
   closeClassName,
}) => {
   const [isOpen, setIsOpen] = useState(false);

   return (
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
         {showButton && (
            <DialogTrigger className='w-full'>
               <div>
                  <Button
                     className={cn('my-4 flex h-10 w-full justify-start text-base font-medium', buttonClassName)}
                     prefix={buttonIcon}
                     variant='ghost'
                     onClick={() => setIsOpen(true)}
                  >
                     {buttonChildren}
                  </Button>
               </div>
            </DialogTrigger>
         )}
         <CreateModalContent
            className={modalClassName}
            closeClassName={closeClassName}
            closeIcon={closeIcon}
            overlayClassName={overlayClassName}
         >
            {React.cloneElement(children as React.ReactElement, { setModalOpen: setIsOpen })}
         </CreateModalContent>
      </Dialog>
   );
};
