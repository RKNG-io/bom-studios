'use client'

import { Section } from '@/components/ui/section'
import { Container } from '@/components/layout/container'
import { StepCard } from '@/components/step-card'
import { useLanguage } from '@/lib/language-context'

export function HowItWorks() {
  const { t } = useLanguage()

  return (
    <Section background="white">
      <Container>
        <h2 className="font-heading text-2xl md:text-3xl text-center mb-12">
          {t.how.headline}
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative">
          {/* Connecting line on desktop */}
          <div className="hidden md:block absolute top-5 left-0 right-0 h-[2px] bg-bom-silver -z-10" />

          {t.how.steps.map((step, index) => (
            <StepCard
              key={index}
              number={index + 1}
              title={step.title}
              description={step.description}
            />
          ))}
        </div>
      </Container>
    </Section>
  )
}

export { HowItWorks as default }
