'use client'

import { Section } from '@/components/ui/section'
import { Container } from '@/components/layout/container'
import { PackageCard } from '@/components/package-card'
import { useLanguage } from '@/lib/language-context'

export function Packages() {
  const { t } = useLanguage()

  return (
    <Section background="warm-white" id="packages">
      <Container>
        <h2 className="font-heading text-2xl md:text-3xl text-center mb-12">
          {t.packages.headline}
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {t.packages.items.map((pkg, index) => (
            <PackageCard
              key={index}
              name={pkg.name}
              price={pkg.price}
              description={pkg.description}
              features={[...pkg.features]}
              highlighted={'highlighted' in pkg && pkg.highlighted}
              ctaText={`${t.packages.chooseCta} ${pkg.name}`}
            />
          ))}
        </div>

        <p className="text-center text-bom-steel text-sm">
          {t.packages.footer}
        </p>
      </Container>
    </Section>
  )
}

export { Packages as default }
