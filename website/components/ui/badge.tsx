import * as React from 'react'
import { cn } from '@/lib/utils'

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  children: React.ReactNode
  variant?: 'default' | 'success' | 'warning' | 'error'
}

export const Badge = ({
  children,
  variant = 'default',
  className,
  ...rest
}: BadgeProps) => {
  const variantClasses = {
    default: 'bg-bom-silver text-bom-slate',
    success: 'bg-bom-sage/20 text-bom-sage',
    warning: 'bg-amber-100 text-amber-800',
    error: 'bg-bom-error/20 text-bom-error',
  }

  return (
    <span
      className={cn(
        'inline-flex px-2 py-1 text-xs font-medium rounded',
        variantClasses[variant],
        className
      )}
      {...rest}
    >
      {children}
    </span>
  )
}
