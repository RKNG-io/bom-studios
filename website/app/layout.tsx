import type { Metadata } from 'next'
import { Inter, Michroma } from 'next/font/google'
import { LanguageProvider } from '@/lib/language-context'
import { AuthProvider } from '@/lib/auth-context'
import { Header } from '@/components/layout/header'
import { Footer } from '@/components/layout/footer'
import './globals.css'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const michroma = Michroma({
  weight: '400',
  subsets: ['latin'],
  variable: '--font-michroma',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'BOM Studios — Social media that actually gets done',
  description:
    'Professional short-form video content for businesses. We handle everything from concept to posting, so you can focus on running your business.',
  openGraph: {
    title: 'BOM Studios — Social media that actually gets done',
    description:
      'Professional short-form video content for businesses. We handle everything from concept to posting, so you can focus on running your business.',
    images: ['/og-image.png'],
    type: 'website',
    locale: 'nl_NL',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'BOM Studios — Social media that actually gets done',
    description:
      'Professional short-form video content for businesses. We handle everything from concept to posting, so you can focus on running your business.',
    images: ['/og-image.png'],
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="nl" className={`${inter.variable} ${michroma.variable}`}>
      <body className="font-body text-bom-black bg-bom-warm-white antialiased">
        <AuthProvider>
          <LanguageProvider>
            <Header />
            {children}
            <Footer />
          </LanguageProvider>
        </AuthProvider>
      </body>
    </html>
  )
}
