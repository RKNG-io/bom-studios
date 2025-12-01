import * as React from 'react'
import { LucideIcon } from 'lucide-react'
import { cn } from '@/lib/utils'

export interface FeatureItemProps {
  icon: LucideIcon
  title: string
  description: string
  className?: string
}

export const FeatureItem = ({
  icon: Icon,
  title,
  description,
  className,
}: FeatureItemProps) => {
  return (
    <div className={cn('text-center space-y-4', className)}>
      <div className="flex justify-center">
        <div className="w-12 h-12 rounded-lg border border-bom-silver bg-bom-paper-white flex items-center justify-center">
          <Icon size={24} className="text-bom-black" strokeWidth={1.5} />
        </div>
      </div>
      <div>
        <h3 className="font-heading text-lg text-bom-black mb-2">{title}</h3>
        <p className="text-sm text-bom-steel leading-relaxed">{description}</p>
      </div>
    </div>
  )
}
