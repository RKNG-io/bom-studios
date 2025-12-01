import * as React from 'react'
import { cn } from '@/lib/utils'

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
  interactive?: boolean
  padding?: 'sm' | 'md' | 'lg'
}

export const Card = ({
  children,
  className,
  interactive = false,
  padding = 'md',
  ...rest
}: CardProps) => {
  const paddingClasses = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  }

  return (
    <div
      className={cn(
        'bg-bom-paper-white border border-bom-silver rounded-lg',
        interactive && 'hover:border-bom-black transition-colors cursor-pointer',
        paddingClasses[padding],
        className
      )}
      {...rest}
    >
      {children}
    </div>
  )
}
