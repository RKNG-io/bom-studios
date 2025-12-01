'use client'

import * as React from 'react'
import Link from 'next/link'
import { X } from 'lucide-react'
import { Button } from '@/components/ui/button'

export interface MobileMenuProps {
  open: boolean
  onClose: () => void
  items: Array<{ label: string; href: string }>
}

export const MobileMenu = ({ open, onClose, items }: MobileMenuProps) => {
  // Close menu on escape key
  React.useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    if (open) {
      document.addEventListener('keydown', handleEscape)
      document.body.style.overflow = 'hidden'
    }
    return () => {
      document.removeEventListener('keydown', handleEscape)
      document.body.style.overflow = 'unset'
    }
  }, [open, onClose])

  if (!open) return null

  return (
    <div
      className="fixed inset-0 z-50 bg-bom-black text-white transition-transform duration-300 ease-in-out"
      style={{
        transform: open ? 'translateX(0)' : 'translateX(100%)',
      }}
    >
      {/* Close Button */}
      <button
        onClick={onClose}
        className="absolute top-4 right-4 p-2 text-white hover:text-bom-silver transition-colors"
        aria-label="Close menu"
      >
        <X className="h-6 w-6" />
      </button>

      {/* Navigation Links */}
      <nav className="flex flex-col items-center justify-center h-full gap-8">
        {items.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            onClick={onClose}
            className="text-2xl font-medium hover:text-bom-silver transition-colors"
          >
            {item.label}
          </Link>
        ))}

        {/* CTA Button */}
        <div className="mt-8">
          <Button variant="primary-inverted" size="lg">
            Start
          </Button>
        </div>
      </nav>
    </div>
  )
}
