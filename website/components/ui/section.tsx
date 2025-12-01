import * as React from 'react'
import { cn } from '@/lib/utils'

export interface SectionProps extends React.HTMLAttributes<HTMLElement> {
  children: React.ReactNode
  background?: 'black' | 'white' | 'warm-white'
}

export const Section = ({
  children,
  background = 'white',
  className,
  id,
  ...rest
}: SectionProps) => {
  const backgroundClasses = {
    black: 'bg-bom-black text-white',
    white: 'bg-white text-bom-black',
    'warm-white': 'bg-bom-warm-white text-bom-black',
  }

  return (
    <section
      id={id}
      className={cn(
        'py-16 md:py-24',
        backgroundClasses[background],
        className
      )}
      {...rest}
    >
      {children}
    </section>
  )
}
