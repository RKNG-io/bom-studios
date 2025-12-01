'use client'

import Link from 'next/link'
import { ArrowRight } from 'lucide-react'
import { Section } from '@/components/ui/section'
import { Container } from '@/components/layout/container'
import { Button } from '@/components/ui/button'
import { useLanguage } from '@/lib/language-context'

export function Hero() {
  const { t } = useLanguage()

  return (
    <Section background="black" className="min-h-[80vh] flex items-center">
      <Container>
        <div className="text-center space-y-8">
          <h1 className="font-heading text-4xl md:text-5xl lg:text-6xl text-white leading-tight">
            {t.hero.headline}
          </h1>

          <p className="text-lg md:text-xl text-bom-silver max-w-2xl mx-auto">
            {t.hero.subheadline}
          </p>

          <Link href="/starten">
            <Button
              variant="primary-inverted"
              className="flex items-center gap-2"
            >
              {t.hero.cta}
              <ArrowRight size={20} />
            </Button>
          </Link>

          <p className="text-sm text-bom-steel">
            {t.hero.microcopy}
          </p>
        </div>
      </Container>
    </Section>
  )
}

export { Hero as default }
