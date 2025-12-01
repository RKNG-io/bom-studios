import Link from 'next/link'
import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'

export interface PackageCardProps {
  name: string
  price: string
  description: string
  features: string[]
  highlighted?: boolean
  ctaText: string
  className?: string
}

export function PackageCard({
  name,
  price,
  description,
  features,
  highlighted = false,
  ctaText,
  className,
}: PackageCardProps) {
  return (
    <div
      className={cn(
        'bg-white rounded-lg p-6 md:p-8 flex flex-col border',
        highlighted
          ? 'border-bom-black shadow-lg'
          : 'border-bom-silver',
        className
      )}
    >
      {/* Header */}
      <div className="mb-6 space-y-2">
        <h3 className="font-heading text-xl text-bom-black">{name}</h3>
        <div className="font-body font-bold text-3xl text-bom-black">{price}</div>
        <p className="text-sm text-bom-steel">{description}</p>
      </div>

      {/* Features */}
      <ul className="space-y-3 mb-8 flex-grow">
        {features.map((feature, index) => (
          <li key={index} className="flex items-start gap-3">
            <Check
              size={20}
              className="text-bom-sage flex-shrink-0 mt-0.5"
              strokeWidth={2}
            />
            <span className="text-sm text-bom-slate">{feature}</span>
          </li>
        ))}
      </ul>

      {/* Button */}
      <Link href="/starten">
        <Button
          variant={highlighted ? 'primary' : 'secondary'}
          className="w-full"
        >
          {ctaText}
        </Button>
      </Link>
    </div>
  )
}

export { PackageCard as default }
