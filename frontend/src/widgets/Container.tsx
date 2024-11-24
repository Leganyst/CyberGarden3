import { cn } from '@/utils/lib/utils';

interface ContainerProps {
   children: React.ReactNode;
   className?: string;
}

export const Container = ({ className, children }: ContainerProps) => {
   return <div className={cn('mx-auto max-w-[1280px]', className)}>{children}</div>;
};
