'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { ArrowRight } from 'lucide-react'
import { Section } from '@/components/ui/section'
import { Container } from '@/components/layout/container'
import { Button } from '@/components/ui/button'
import { useLanguage } from '@/lib/language-context'

export function FinalCta() {
  const [input, setInput] = useState('')
  const router = useRouter()
  const { t } = useLanguage()

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    router.push(`/starten?ref=${encodeURIComponent(input)}`)
  }

  return (
    <Section background="black">
      <Container>
        <div className="flex flex-col items-center text-center">
          <h2 className="font-heading text-3xl md:text-4xl text-white mb-8">
            {t.finalCta.headline}
          </h2>

          <form onSubmit={handleSubmit} className="w-full max-w-md mb-4">
            <div className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={t.hero.placeholder}
                className="flex-1 px-4 py-3 rounded bg-white text-bom-black focus:outline-none focus:ring-2 focus:ring-bom-blue"
              />
              <Button type="submit" variant="primary-inverted">
                {t.hero.cta}
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </div>
          </form>

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
