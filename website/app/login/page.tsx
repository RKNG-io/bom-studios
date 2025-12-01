'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Section } from '@/components/ui/section'
import { Container } from '@/components/layout/container'
import { Button } from '@/components/ui/button'
import { useLanguage } from '@/lib/language-context'
import { useAuth } from '@/lib/auth-context'
import { Mail, CheckCircle, Loader2 } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || ''

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState<'idle' | 'loading' | 'sent' | 'verifying' | 'error'>('idle')
  const [error, setError] = useState('')
  const { t, language } = useLanguage()
  const { login, user } = useAuth()
  const router = useRouter()
  const searchParams = useSearchParams()

  // Handle magic link token verification
  useEffect(() => {
    const token = searchParams.get('token')
    if (token) {
      verifyToken(token)
    }
  }, [searchParams])

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      router.push('/dashboard')
    }
  }, [user, router])

  async function verifyToken(token: string) {
    setStatus('verifying')
    try {
      const res = await fetch(`${API_URL}/api/auth/verify?token=${token}`)
      if (res.ok) {
        const data = await res.json()
        await login(data.access_token)
      } else {
        setError(language === 'nl' ? 'Ongeldige of verlopen link' : 'Invalid or expired link')
        setStatus('error')
      }
    } catch {
      setError(language === 'nl' ? 'Kon niet verifiëren' : 'Could not verify')
      setStatus('error')
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setStatus('loading')
    setError('')

    try {
      const res = await fetch(`${API_URL}/api/auth/magic-link`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      })

      if (res.ok) {
        setStatus('sent')
      } else {
        const data = await res.json()
        setError(data.detail || (language === 'nl' ? 'Kon geen link versturen' : 'Could not send link'))
        setStatus('error')
      }
    } catch {
      setError(language === 'nl' ? 'Verbindingsfout' : 'Connection error')
      setStatus('error')
    }
  }

  const content = {
    en: {
      title: 'Client Portal',
      subtitle: 'View your projects and approve videos',
      emailLabel: 'Email address',
      emailPlaceholder: 'you@company.com',
      sendLink: 'Send login link',
      sending: 'Sending...',
      verifying: 'Verifying...',
      sentTitle: 'Check your email',
      sentMessage: 'We sent a login link to',
      sentNote: 'Click the link to access your dashboard.',
      tryAgain: 'Try again',
    },
    nl: {
      title: 'Klantportaal',
      subtitle: 'Bekijk je projecten en keur video\'s goed',
      emailLabel: 'E-mailadres',
      emailPlaceholder: 'jij@bedrijf.nl',
      sendLink: 'Verstuur login link',
      sending: 'Versturen...',
      verifying: 'Verifiëren...',
      sentTitle: 'Check je e-mail',
      sentMessage: 'We hebben een login link gestuurd naar',
      sentNote: 'Klik op de link om naar je dashboard te gaan.',
      tryAgain: 'Opnieuw proberen',
    },
  }

  const c = content[language]

  if (status === 'verifying') {
    return (
      <Section background="warm-white" className="min-h-[60vh] flex items-center">
        <Container>
          <div className="max-w-md mx-auto text-center">
            <Loader2 className="w-12 h-12 text-bom-blue animate-spin mx-auto mb-4" />
            <p className="text-lg text-bom-graphite">{c.verifying}</p>
          </div>
        </Container>
      </Section>
    )
  }

  if (status === 'sent') {
    return (
      <Section background="warm-white" className="min-h-[60vh] flex items-center">
        <Container>
          <div className="max-w-md mx-auto text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
            <h1 className="font-heading text-2xl md:text-3xl text-bom-black mb-4">
              {c.sentTitle}
            </h1>
            <p className="text-bom-graphite mb-2">
              {c.sentMessage} <strong>{email}</strong>
            </p>
            <p className="text-bom-steel text-sm mb-8">
              {c.sentNote}
            </p>
            <button
              onClick={() => {
                setStatus('idle')
                setEmail('')
              }}
              className="text-bom-blue underline hover:text-bom-black"
            >
              {c.tryAgain}
            </button>
          </div>
        </Container>
      </Section>
    )
  }

  return (
    <Section background="warm-white" className="min-h-[60vh] flex items-center">
      <Container>
        <div className="max-w-md mx-auto">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-bom-black rounded-full flex items-center justify-center mx-auto mb-6">
              <Mail className="w-8 h-8 text-white" />
            </div>
            <h1 className="font-heading text-2xl md:text-3xl text-bom-black mb-2">
              {c.title}
            </h1>
            <p className="text-bom-graphite">
              {c.subtitle}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-bom-black mb-2">
                {c.emailLabel}
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder={c.emailPlaceholder}
                required
                className="w-full px-4 py-3 rounded border border-bom-silver focus:outline-none focus:ring-2 focus:ring-bom-blue focus:border-transparent"
              />
            </div>

            {error && (
              <p className="text-red-600 text-sm">{error}</p>
            )}

            <Button
              type="submit"
              disabled={status === 'loading'}
              className="w-full"
            >
              {status === 'loading' ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin mr-2" />
                  {c.sending}
                </>
              ) : (
                c.sendLink
              )}
            </Button>
          </form>
        </div>
      </Container>
    </Section>
  )
}
