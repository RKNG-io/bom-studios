'use client'

import Link from 'next/link'
import { ArrowRight } from 'lucide-react'
import { Section } from '@/components/ui/section'
import { Container } from '@/components/layout/container'
import { Button } from '@/components/ui/button'
import { useLanguage } from '@/lib/language-context'

export function FinalCta() {
  const { t } = useLanguage()

  return (
    <Section background="black">
      <Container>
        <div className="flex flex-col items-center text-center">
          <h2 className="font-heading text-3xl md:text-4xl text-white mb-8">
            {t.finalCta.headline}
          </h2>

          <Link href="/starten" className="mb-4">
            <Button variant="primary-inverted">
              {t.hero.cta}
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>

          <a
            href="/contact"
            className="text-bom-blue underline hover:text-bom-silver"
          >
            {t.finalCta.link}
          </a>
        </div>
      </Container>
    </Section>
  )
}

export { FinalCta as default }
