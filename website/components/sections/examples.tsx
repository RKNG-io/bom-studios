'use client'

import Link from 'next/link'
import { Play } from 'lucide-react'
import { Section } from '@/components/ui/section'
import { Container } from '@/components/layout/container'
import { useLanguage } from '@/lib/language-context'

export function Examples() {
  const { t } = useLanguage()

  return (
    <Section background="white" id="examples">
      <Container>
        <h2 className="font-heading text-2xl md:text-3xl text-center mb-8">
          {t.examples.headline}
        </h2>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
          {Array.from({ length: 6 }).map((_, index) => (
            <div
              key={index}
              className="aspect-[9/16] bg-bom-silver rounded-lg flex items-center justify-center"
            >
              <Play className="h-12 w-12 text-white" fill="currentColor" />
            </div>
          ))}
        </div>

        <div className="text-center">
          <Link
            href="/voorbeelden"
            className="text-bom-blue underline hover:text-bom-black"
          >
            {t.examples.cta}
          </Link>
        </div>
      </Container>
    </Section>
  )
}

export { Examples as default }
