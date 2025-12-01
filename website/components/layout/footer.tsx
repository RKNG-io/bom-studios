'use client'

import Link from 'next/link'
import { Instagram, Mail } from 'lucide-react'
import { Container } from './container'
import { useLanguage } from '@/lib/language-context'

export function Footer() {
  const { t } = useLanguage()

  return (
    <footer className="bg-bom-black text-white py-12 md:py-16">
      <Container>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12 mb-8">
          {/* Brand */}
          <div>
            <Link href="/" className="font-heading text-xl mb-4 block">
              BOM Studios
            </Link>
            <p className="text-bom-steel text-sm">
              {t.footer.tagline}
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="font-body font-medium mb-4">{t.footer.links}</h4>
            <ul className="space-y-2">
              <li>
                <Link href="/#examples" className="text-bom-steel hover:text-white transition-colors text-sm">
                  {t.nav.examples}
                </Link>
              </li>
              <li>
                <Link href="/#packages" className="text-bom-steel hover:text-white transition-colors text-sm">
                  {t.nav.pricing}
                </Link>
              </li>
              <li>
                <Link href="/#about" className="text-bom-steel hover:text-white transition-colors text-sm">
                  {t.nav.about}
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-bom-steel hover:text-white transition-colors text-sm">
                  {t.nav.contact}
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-body font-medium mb-4">{t.footer.contact}</h4>
            <ul className="space-y-2">
              <li>
                <a
                  href="https://instagram.com/bomstudios"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-bom-steel hover:text-white transition-colors text-sm flex items-center gap-2"
                >
                  <Instagram size={16} />
                  Instagram
                </a>
              </li>
              <li>
                <a
                  href="mailto:hello@bomstudios.nl"
                  className="text-bom-steel hover:text-white transition-colors text-sm flex items-center gap-2"
                >
                  <Mail size={16} />
                  Email
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="pt-8 border-t border-bom-slate/30">
          <p className="text-bom-steel text-sm">{t.footer.copyright}</p>
        </div>
      </Container>
    </footer>
  )
}

export { Footer as default }
