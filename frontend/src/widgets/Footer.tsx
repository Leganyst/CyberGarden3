import { cn } from '@/utils/lib/utils';

interface FooterProps {
   className?: string;
}

export const Footer = ({ className }: FooterProps) => {
   return <div className={cn('', className)}></div>;
};
