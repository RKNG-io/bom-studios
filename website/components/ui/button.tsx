import * as React from 'react'
import { cn } from '@/lib/utils'

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'text' | 'primary-inverted'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', className, children, ...rest }, ref) => {
    const variantClasses = {
      primary: 'bg-bom-black text-white hover:bg-bom-slate',
      'primary-inverted': 'bg-white text-bom-black hover:bg-bom-silver',
      secondary:
        'border border-bom-black text-bom-black hover:bg-bom-black hover:text-white',
      text: 'text-bom-blue underline hover:text-bom-black',
    }

    const sizeClasses = {
      sm: 'px-4 py-2 text-sm',
      md: 'px-6 py-3 text-base',
      lg: 'px-8 py-4 text-lg',
    }

    return (
      <button
        ref={ref}
        className={cn(
          'rounded font-medium transition-colors',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-bom-blue focus-visible:ring-offset-2',
          'disabled:opacity-50 disabled:pointer-events-none',
          variantClasses[variant],
          sizeClasses[size],
          className
        )}
        {...rest}
      >
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'
