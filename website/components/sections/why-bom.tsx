'use client'

import {
  Calendar,
  Sparkles,
  MessageSquareOff,
  Zap,
  Globe,
  Receipt,
} from 'lucide-react'
import { Section } from '@/components/ui/section'
import { Container } from '@/components/layout/container'
import { FeatureItem } from '@/components/feature-item'
import { useLanguage } from '@/lib/language-context'

const icons = [Calendar, Sparkles, MessageSquareOff, Zap, Globe, Receipt]

export function WhyBom() {
  const { t } = useLanguage()

  return (
    <Section background="warm-white">
      <Container>
        <h2 className="font-heading text-2xl md:text-3xl text-center mb-12">
          {t.why.headline}
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-12">
          {t.why.features.map((feature, index) => (
            <FeatureItem
              key={index}
              icon={icons[index]}
              title={feature.title}
              description={feature.description}
            />
          ))}
        </div>
      </Container>
    </Section>
  )
}

export { WhyBom as default }
