'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { ArrowRight } from 'lucide-react'
import { Section } from '@/components/ui/section'
import { Container } from '@/components/layout/container'
import { Button } from '@/components/ui/button'
import { useLanguage } from '@/lib/language-context'

export function Hero() {
  const [input, setInput] = useState('')
  const router = useRouter()
  const { t } = useLanguage()

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    router.push(`/starten?ref=${encodeURIComponent(input)}`)
  }

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

          <form
            onSubmit={handleSubmit}
            className="flex flex-col sm:flex-row gap-4 max-w-lg mx-auto"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={t.hero.placeholder}
              className="flex-1 px-4 py-3 rounded text-bom-black focus:outline-none focus:ring-2 focus:ring-bom-blue"
            />
            <Button
              type="submit"
              variant="primary-inverted"
              className="flex items-center gap-2"
            >
              {t.hero.cta}
              <ArrowRight size={20} />
            </Button>
          </form>

          <p className="text-sm text-bom-steel">
            {t.hero.microcopy}
          </p>
        </div>
      </Container>
    </Section>
  )
}

export { Hero as default }
