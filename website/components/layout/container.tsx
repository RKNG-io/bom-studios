import * as React from 'react'
import { cn } from '@/lib/utils'

export interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
  narrow?: boolean
}

export const Container = ({
  children,
  narrow = false,
  className,
  ...rest
}: ContainerProps) => {
  return (
    <div
      className={cn(
        'mx-auto px-4 md:px-12 w-full',
        narrow ? 'max-w-prose' : 'max-w-content',
        className
      )}
      {...rest}
    >
      {children}
    </div>
  )
}
