'use client'

import * as React from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Menu, Globe, User } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Container } from './container'
import { MobileMenu } from './mobile-menu'
import { useLanguage } from '@/lib/language-context'
import { useAuth } from '@/lib/auth-context'

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false)
  const { language, setLanguage, t } = useLanguage()
  const { user } = useAuth()

  const navItems = [
    { label: t.nav.examples, href: '/#examples' },
    { label: t.nav.pricing, href: '/#packages' },
    { label: t.nav.about, href: '/#about' },
  ]

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'nl' : 'en')
  }

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-bom-silver">
      <Container>
        <nav className="flex items-center justify-between h-16 md:h-20">
          {/* Logo */}
          <Link href="/" className="flex items-center">
            <Image
              src="/images/logo.png"
              alt="BOM Studios"
              width={180}
              height={50}
              className="h-12 md:h-14 w-auto"
              priority
            />
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-8">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="text-bom-slate hover:text-bom-black transition-colors font-body"
              >
                {item.label}
              </Link>
            ))}

            {/* Language Toggle */}
            <button
              onClick={toggleLanguage}
              className="flex items-center gap-1.5 text-bom-steel hover:text-bom-black transition-colors"
              aria-label="Toggle language"
            >
              <Globe size={18} />
              <span className="text-sm font-medium uppercase">{language}</span>
            </button>

            {user ? (
              <Link
                href="/dashboard"
                className="flex items-center gap-2 text-bom-graphite hover:text-bom-black transition-colors"
              >
                <User size={18} />
                <span className="text-sm">{language === 'nl' ? 'Dashboard' : 'Dashboard'}</span>
              </Link>
            ) : (
              <Link
                href="/login"
                className="text-bom-graphite hover:text-bom-black transition-colors text-sm"
              >
                {language === 'nl' ? 'Inloggen' : 'Login'}
              </Link>
            )}

            <Link href="/starten">
              <Button>{t.nav.start}</Button>
            </Link>
          </div>

          {/* Mobile: Language + Menu */}
          <div className="flex md:hidden items-center gap-2">
            <button
              onClick={toggleLanguage}
              className="p-2 text-bom-steel hover:text-bom-black"
              aria-label="Toggle language"
            >
              <Globe size={20} />
            </button>
            <button
              className="p-2"
              onClick={() => setMobileMenuOpen(true)}
              aria-label="Open menu"
            >
              <Menu size={24} />
            </button>
          </div>
        </nav>
      </Container>

      {/* Mobile Menu */}
      <MobileMenu
        open={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
        items={navItems}
      />
    </header>
  )
}
