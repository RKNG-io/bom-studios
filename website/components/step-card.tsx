import * as React from 'react'
import { cn } from '@/lib/utils'

export interface StepCardProps {
  number: number
  title: string
  description: string
  className?: string
}

export const StepCard = ({
  number,
  title,
  description,
  className,
}: StepCardProps) => {
  return (
    <div className={cn('space-y-4', className)}>
      <div className="flex justify-center md:justify-start">
        <div className="w-10 h-10 rounded-full bg-bom-black text-white flex items-center justify-center font-heading text-lg">
          {number}
        </div>
      </div>
      <div className="text-center md:text-left">
        <h3 className="font-heading text-lg text-bom-black mb-2">{title}</h3>
        <p className="text-sm text-bom-steel leading-relaxed">{description}</p>
      </div>
    </div>
  )
}
