'use client'

import { Section } from '@/components/ui/section'
import { Container } from '@/components/layout/container'
import { useLanguage } from '@/lib/language-context'

export function About() {
  const { t } = useLanguage()

  return (
    <Section background="warm-white" id="about">
      <Container>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12 items-center">
          <div className="aspect-square bg-bom-silver rounded-lg" />

          <div className="space-y-4">
            <h2 className="font-heading text-2xl">{t.about.headline}</h2>
            {t.about.paragraphs.map((paragraph, index) => (
              <p key={index} className="text-bom-black">
                {paragraph}
              </p>
            ))}
          </div>
        </div>
      </Container>
    </Section>
  )
}

export { About as default }
