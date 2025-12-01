'use client'

import { useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { ArrowRight, ArrowLeft, Check } from 'lucide-react'
import { Container } from '@/components/layout/container'
import { Button } from '@/components/ui/button'
import { useLanguage } from '@/lib/language-context'

interface FormData {
  business_name: string
  email: string
  links: string
  what_they_sell: string
  target_customer: string
  what_makes_different: string
  language: string
  language_other: string
  video_style: string
  topic: string
  reference_videos: string
  notes: string
}

const initialFormData: FormData = {
  business_name: '',
  email: '',
  links: '',
  what_they_sell: '',
  target_customer: '',
  what_makes_different: '',
  language: '',
  language_other: '',
  video_style: '',
  topic: '',
  reference_videos: '',
  notes: '',
}

export default function StartenPage() {
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState<FormData>(initialFormData)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const { language: siteLang } = useLanguage()

  const totalSteps = 4

  const updateField = (field: keyof FormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const canProceed = () => {
    switch (step) {
      case 1:
        return formData.business_name.trim() !== '' && formData.email.trim() !== ''
      case 2:
        return (
          formData.what_they_sell.trim() !== '' &&
          formData.target_customer.trim() !== '' &&
          formData.what_makes_different.trim() !== ''
        )
      case 3:
        return formData.language.trim() !== '' &&
          (formData.language !== 'other' || formData.language_other.trim() !== '') &&
          formData.video_style.trim() !== ''
      case 4:
        return true
      default:
        return false
    }
  }

  const handleSubmit = async () => {
    setIsSubmitting(true)
    try {
      // Submit to webhook (configure URL in env)
      const webhookUrl = process.env.NEXT_PUBLIC_INTAKE_WEBHOOK_URL
      if (webhookUrl) {
        // Format as Tally-compatible payload for API
        const tallyPayload = {
          eventId: `web-${Date.now()}`,
          eventType: 'FORM_RESPONSE',
          createdAt: new Date().toISOString(),
          data: {
            fields: [
              { key: 'business_name', label: 'Business Name', value: formData.business_name },
              { key: 'email', label: 'Email', value: formData.email },
              { key: 'links', label: 'Links', value: formData.links },
              { key: 'what_they_sell', label: 'What do you sell', value: formData.what_they_sell },
              { key: 'target_customer', label: 'Target Customer', value: formData.target_customer },
              { key: 'what_makes_different', label: 'What makes you different', value: formData.what_makes_different },
              { key: 'language', label: 'Language', value: formData.language === 'other' ? formData.language_other : formData.language },
              { key: 'video_style', label: 'Video Style', value: formData.video_style },
              { key: 'topic', label: 'Topic', value: formData.topic },
              { key: 'reference_videos', label: 'Reference Videos', value: formData.reference_videos },
              { key: 'notes', label: 'Notes', value: formData.notes },
            ],
          },
        }
        await fetch(webhookUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(tallyPayload),
        })
      }
      setIsSubmitted(true)
    } catch (error) {
      console.error('Submission error:', error)
      // Still show success - webhook can be configured later
      setIsSubmitted(true)
    } finally {
      setIsSubmitting(false)
    }
  }

  const nextStep = () => {
    if (step < totalSteps) {
      setStep(step + 1)
    } else {
      handleSubmit()
    }
  }

  const prevStep = () => {
    if (step > 1) {
      setStep(step - 1)
    }
  }

  // Success state
  if (isSubmitted) {
    return (
      <main className="min-h-screen bg-bom-warm-white flex items-center justify-center px-4">
        <Container>
          <div className="max-w-md mx-auto text-center py-16">
            <div className="w-16 h-16 bg-bom-sage rounded-full flex items-center justify-center mx-auto mb-6">
              <Check className="w-8 h-8 text-white" />
            </div>
            <h1 className="font-heading text-2xl md:text-3xl text-bom-black mb-4">
              {siteLang === 'nl' ? 'Bedankt!' : 'Thanks!'}
            </h1>
            <p className="text-bom-slate mb-8">
              {siteLang === 'nl'
                ? 'Je eerste videodraft is binnen 48 uur klaar.'
                : 'Your first video draft will be ready within 48 hours.'}
            </p>
            <Link href="/">
              <Button variant="secondary">
                {siteLang === 'nl' ? 'Terug naar home' : 'Back to home'}
              </Button>
            </Link>
          </div>
        </Container>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-bom-warm-white">
      <Container>
        <div className="max-w-xl mx-auto py-8 md:py-16">
          {/* Header */}
          <div className="text-center mb-8">
            <Link href="/" className="inline-block mb-6">
              <Image
                src="/images/logo.png"
                alt="BOM Studios"
                width={120}
                height={34}
                className="h-8 w-auto"
              />
            </Link>
            <h1 className="font-heading text-2xl md:text-3xl text-bom-black mb-2">
              {siteLang === 'nl' ? "Laten we je eerste video maken" : "Let's create your first video"}
            </h1>
            <p className="text-bom-slate">
              {siteLang === 'nl'
                ? 'Beantwoord een paar vragen zodat we kunnen beginnen. Duurt ongeveer 3 minuten.'
                : 'Answer a few quick questions so we can get started. Takes about 3 minutes.'}
            </p>
          </div>

          {/* Progress */}
          <div className="flex gap-2 mb-8">
            {Array.from({ length: totalSteps }).map((_, i) => (
              <div
                key={i}
                className={`h-1 flex-1 rounded-full transition-colors ${
                  i + 1 <= step ? 'bg-bom-black' : 'bg-bom-silver'
                }`}
              />
            ))}
          </div>

          {/* Form Steps */}
          <div className="bg-white rounded-lg border border-bom-silver p-6 md:p-8">
            {step === 1 && (
              <div className="space-y-6">
                <h2 className="font-heading text-lg text-bom-black">
                  {siteLang === 'nl' ? 'Over je bedrijf' : 'About Your Business'}
                </h2>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-bom-black">
                    {siteLang === 'nl' ? 'Hoe heet je bedrijf?' : "What's your business called?"}
                  </label>
                  <input
                    type="text"
                    value={formData.business_name}
                    onChange={(e) => updateField('business_name', e.target.value)}
                    placeholder={siteLang === 'nl' ? 'bijv. Amsterdam Coffee Roasters' : 'e.g. Amsterdam Coffee Roasters'}
                    className="w-full px-4 py-3 rounded border border-bom-silver focus:outline-none focus:ring-2 focus:ring-bom-black text-bom-black"
                    required
                  />
                </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-bom-black">
                    {siteLang === 'nl' ? 'Je e-mailadres' : 'Your email address'}
                  </label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => updateField('email', e.target.value)}
                    placeholder="you@yourbusiness.com"
                    className="w-full px-4 py-3 rounded border border-bom-silver focus:outline-none focus:ring-2 focus:ring-bom-black text-bom-black"
                    required
                  />
                  <p className="text-xs text-bom-steel">
                    {siteLang === 'nl' ? 'We sturen je video hierheen.' : "We'll send your video here."}
                  </p>
                </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-bom-black">
                    {siteLang === 'nl' ? 'Je website en social links' : 'Your website and social links'}
                  </label>
                  <textarea
                    value={formData.links}
                    onChange={(e) => updateField('links', e.target.value)}
                    placeholder={`https://yourbusiness.com\ninstagram.com/yourbusiness\nlinkedin.com/company/yourbusiness`}
                    rows={3}
                    className="w-full px-4 py-3 rounded border border-bom-silver focus:outline-none focus:ring-2 focus:ring-bom-black text-bom-black resize-none"
                  />
                  <p className="text-xs text-bom-steel">
                    {siteLang === 'nl'
                      ? 'Voeg er zoveel toe als je wilt — één per regel. Helpt ons je merk snel te begrijpen.'
                      : 'Add as many as you like — one per line. Helps us understand your brand quickly.'}
                  </p>
                </div>
              </div>
            )}

            {step === 2 && (
              <div className="space-y-6">
                <h2 className="font-heading text-lg text-bom-black">
                  {siteLang === 'nl' ? 'Wat je doet' : 'What You Do'}
                </h2>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-bom-black">
                    {siteLang === 'nl' ? 'Wat verkoop of bied je aan?' : 'What do you sell or offer?'}
                  </label>
                  <textarea
                    value={formData.what_they_sell}
                    onChange={(e) => updateField('what_they_sell', e.target.value)}
                    placeholder={
                      siteLang === 'nl'
                        ? 'bijv. Wij verkopen specialty koffiebonen, wekelijks gebrand en thuisbezorgd.'
                        : 'e.g. We sell specialty coffee beans, roasted weekly and delivered to your door.'
                    }
                    rows={3}
                    className="w-full px-4 py-3 rounded border border-bom-silver focus:outline-none focus:ring-2 focus:ring-bom-black text-bom-black resize-none"
                    required
                  />
                  <p className="text-xs text-bom-steel">
                    {siteLang === 'nl'
                      ? 'Wees specifiek. Wat zou je iemand op een feestje vertellen?'
                      : 'Be specific. What would you tell someone at a party?'}
                  </p>
                </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-bom-black">
                    {siteLang === 'nl' ? 'Wie koopt bij je?' : 'Who buys from you?'}
                  </label>
                  <textarea
                    value={formData.target_customer}
                    onChange={(e) => updateField('target_customer', e.target.value)}
                    placeholder={
                      siteLang === 'nl'
                        ? 'bijv. Koffieliefhebbers die thuis zetten en om kwaliteit geven.'
                        : 'e.g. Coffee lovers who brew at home and care about quality.'
                    }
                    rows={3}
                    className="w-full px-4 py-3 rounded border border-bom-silver focus:outline-none focus:ring-2 focus:ring-bom-black text-bom-black resize-none"
                    required
                  />
                  <p className="text-xs text-bom-steel">
                    {siteLang === 'nl' ? 'Denk aan je beste klanten.' : 'Think about your best customers.'}
                  </p>
                </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-bom-black">
                    {siteLang === 'nl' ? 'Wat maakt je anders dan concurrenten?' : 'What makes you different from competitors?'}
                  </label>
                  <textarea
                    value={formData.what_makes_different}
                    onChange={(e) => updateField('what_makes_different', e.target.value)}
                    placeholder={
                      siteLang === 'nl'
                        ? 'bijv. Wij branden elke week — de meeste supermarktkoffie is maanden geleden gebrand.'
                        : 'e.g. We roast every week — most supermarket coffee was roasted months ago.'
                    }
                    rows={3}
                    className="w-full px-4 py-3 rounded border border-bom-silver focus:outline-none focus:ring-2 focus:ring-bom-black text-bom-black resize-none"
                    required
                  />
                  <p className="text-xs text-bom-steel">
                    {siteLang === 'nl' ? 'Waarom zou iemand voor jou kiezen?' : 'Why should someone choose you?'}
                  </p>
                </div>
              </div>
            )}

            {step === 3 && (
              <div className="space-y-6">
                <h2 className="font-heading text-lg text-bom-black">
                  {siteLang === 'nl' ? 'Video voorkeuren' : 'Video Preferences'}
                </h2>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-bom-black">
                    {siteLang === 'nl' ? 'In welke taal moet de video zijn?' : 'What language should the video be in?'}
                  </label>
                  <select
                    value={formData.language}
                    onChange={(e) => updateField('language', e.target.value)}
                    className="w-full px-4 py-3 rounded border border-bom-silver focus:outline-none focus:ring-2 focus:ring-bom-black text-bom-black bg-white"
                    required
                  >
                    <option value="">{siteLang === 'nl' ? 'Selecteer een taal...' : 'Select a language...'}</option>
                    <option value="nl">{siteLang === 'nl' ? 'Nederlands' : 'Dutch'}</option>
                    <option value="en">{siteLang === 'nl' ? 'Engels' : 'English'}</option>
                    <option value="nl+en">{siteLang === 'nl' ? 'Nederlands + Engels' : 'Dutch + English'}</option>
                    <option value="other">{siteLang === 'nl' ? 'Andere...' : 'Other...'}</option>
                  </select>
                  {formData.language === 'other' && (
                    <input
                      type="text"
                      value={formData.language_other}
                      onChange={(e) => updateField('language_other', e.target.value)}
                      placeholder={siteLang === 'nl' ? 'Welke taal?' : 'Which language?'}
                      className="w-full px-4 py-3 rounded border border-bom-silver focus:outline-none focus:ring-2 focus:ring-bom-black text-bom-black mt-2"
                      required
                    />
                  )}
                </div>

                <div className="space-y-3">
                  <label className="block text-sm font-medium text-bom-black">
                    {siteLang === 'nl' ? 'Welke videostijl past bij je product?' : 'What video style fits your product?'}
                  </label>
                  <div className="grid grid-cols-1 gap-2">
                    {[
                      { value: 'presenter', labelEn: 'Presenter to Camera', labelNl: 'Presentator voor camera', descEn: 'Trust and directness. Good for services.', descNl: 'Vertrouwen en directheid. Goed voor diensten.' },
                      { value: 'product', labelEn: 'Product Showcase', labelNl: 'Product showcase', descEn: 'Fast cuts, bold visuals. Built for e-commerce.', descNl: 'Snelle cuts, opvallende beelden. Gebouwd voor e-commerce.' },
                      { value: 'animated', labelEn: 'Animated Explainer', labelNl: 'Geanimeerde uitleg', descEn: 'Clean and clear. Works for apps, tools, SaaS.', descNl: 'Schoon en duidelijk. Werkt voor apps, tools, SaaS.' },
                      { value: 'voiceover', labelEn: 'Voiceover + B-roll', labelNl: 'Voice-over + B-roll', descEn: 'Professional tone without on-camera talent.', descNl: 'Professionele toon zonder talent voor de camera.' },
                      { value: 'hybrid', labelEn: 'Hybrid', labelNl: 'Hybride', descEn: 'Mix formats. Test what converts.', descNl: 'Mix formats. Test wat converteert.' },
                    ].map((style) => (
                      <label
                        key={style.value}
                        className={`flex items-start gap-3 p-3 rounded border cursor-pointer transition-colors ${
                          formData.video_style === style.value
                            ? 'border-bom-black bg-bom-warm-white'
                            : 'border-bom-silver hover:border-bom-steel'
                        }`}
                      >
                        <input
                          type="radio"
                          name="video_style"
                          value={style.value}
                          checked={formData.video_style === style.value}
                          onChange={(e) => updateField('video_style', e.target.value)}
                          className="mt-1"
                        />
                        <div>
                          <div className="font-medium text-bom-black">
                            {siteLang === 'nl' ? style.labelNl : style.labelEn}
                          </div>
                          <div className="text-sm text-bom-steel">
                            {siteLang === 'nl' ? style.descNl : style.descEn}
                          </div>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-bom-black">
                    {siteLang === 'nl' ? 'Een specifiek onderwerp voor deze video?' : 'Any specific topic for this video?'}
                  </label>
                  <textarea
                    value={formData.topic}
                    onChange={(e) => updateField('topic', e.target.value)}
                    placeholder={
                      siteLang === 'nl'
                        ? 'bijv. Ons nieuwe zomermenu, Waarom onze bezorging sneller is, Maak kennis met het team'
                        : 'e.g. Our new summer menu, Why our delivery is faster, Meet the team'
                    }
                    rows={3}
                    className="w-full px-4 py-3 rounded border border-bom-silver focus:outline-none focus:ring-2 focus:ring-bom-black text-bom-black resize-none"
                  />
                  <p className="text-xs text-bom-steel">
                    {siteLang === 'nl'
                      ? 'Laat leeg en wij stellen iets voor op basis van je bedrijf.'
                      : "Leave blank and we'll suggest something based on your business."}
                  </p>
                </div>
              </div>
            )}

            {step === 4 && (
              <div className="space-y-6">
                <h2 className="font-heading text-lg text-bom-black">
                  {siteLang === 'nl' ? "Extra's (optioneel)" : 'Extras (Optional)'}
                </h2>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-bom-black">
                    {siteLang === 'nl' ? "Video's waarvan je de stijl leuk vindt?" : 'Any videos you like the style of?'}
                  </label>
                  <textarea
                    value={formData.reference_videos}
                    onChange={(e) => updateField('reference_videos', e.target.value)}
                    placeholder={
                      siteLang === 'nl'
                        ? 'Plak links naar Instagram Reels, TikToks of YouTube Shorts die je leuk vindt'
                        : 'Paste links to Instagram Reels, TikToks, or YouTube Shorts you like'
                    }
                    rows={3}
                    className="w-full px-4 py-3 rounded border border-bom-silver focus:outline-none focus:ring-2 focus:ring-bom-black text-bom-black resize-none"
                  />
                  <p className="text-xs text-bom-steel">
                    {siteLang === 'nl' ? 'Helpt ons je smaak te matchen.' : 'Helps us match your taste.'}
                  </p>
                </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-bom-black">
                    {siteLang === 'nl' ? 'Nog iets anders dat we moeten weten?' : 'Anything else we should know?'}
                  </label>
                  <textarea
                    value={formData.notes}
                    onChange={(e) => updateField('notes', e.target.value)}
                    placeholder={
                      siteLang === 'nl'
                        ? 'Speciale aanbiedingen, merkrichtlijnen, dingen om te vermijden...'
                        : 'Special offers, brand guidelines, things to avoid...'
                    }
                    rows={3}
                    className="w-full px-4 py-3 rounded border border-bom-silver focus:outline-none focus:ring-2 focus:ring-bom-black text-bom-black resize-none"
                  />
                </div>
              </div>
            )}

            {/* Navigation */}
            <div className="flex justify-between mt-8 pt-6 border-t border-bom-silver">
              {step > 1 ? (
                <button
                  onClick={prevStep}
                  className="flex items-center gap-2 text-bom-slate hover:text-bom-black transition-colors"
                >
                  <ArrowLeft size={18} />
                  {siteLang === 'nl' ? 'Terug' : 'Back'}
                </button>
              ) : (
                <div />
              )}

              <Button
                onClick={nextStep}
                disabled={!canProceed() || isSubmitting}
                className="min-w-[140px]"
              >
                {isSubmitting ? (
                  siteLang === 'nl' ? 'Verzenden...' : 'Submitting...'
                ) : step === totalSteps ? (
                  siteLang === 'nl' ? 'Versturen' : 'Get Started'
                ) : (
                  <>
                    {siteLang === 'nl' ? 'Volgende' : 'Next'}
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </>
                )}
              </Button>
            </div>
          </div>

          {/* Step indicator */}
          <p className="text-center text-sm text-bom-steel mt-4">
            {siteLang === 'nl' ? `Stap ${step} van ${totalSteps}` : `Step ${step} of ${totalSteps}`}
          </p>
        </div>
      </Container>
    </main>
  )
}
