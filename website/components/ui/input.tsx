import * as React from 'react'
import { cn } from '@/lib/utils'

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className, ...rest }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-bom-black mb-2">
            {label}
          </label>
        )}
        <input
          ref={ref}
          className={cn(
            'w-full px-4 py-3 rounded bg-white border border-bom-silver',
            'focus:outline-none focus:border-bom-black',
            'placeholder:text-bom-steel',
            'transition-colors',
            error && 'border-bom-error',
            className
          )}
          {...rest}
        />
        {error && (
          <p className="mt-2 text-sm text-bom-error">{error}</p>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'
