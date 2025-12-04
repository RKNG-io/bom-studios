# SKILL.md — Website Agent

## Role

Build and maintain the public marketing website for BOM Studios. This is the landing site where prospective clients learn about the service, view packages, see examples, and sign up.

---

## Scope

- `website/` directory only
- Public marketing pages (no authentication)
- Lead capture form integration (Tally embed or custom)
- SEO optimisation
- Responsive design (mobile-first)

**Out of scope:** Client portal (authenticated), Flet engine, FastAPI backend, n8n workflows

---

## Tech Stack

- Next.js 14 (App Router)
- TypeScript (strict)
- Tailwind CSS
- CSS Modules (for complex animations only)
- Lucide React (icons)
- next/font (Michroma + Inter)
- Vercel (deployment)

---

## Design Principles

From brand kit:

1. **Professional, not flashy** — Clean European aesthetic
2. **Calm, not cold** — Warm whites, subtle movement
3. **Direct, not blunt** — Short sentences, no jargon
4. **Consistent** — 8px spacing grid, limited colour palette
5. **Fast** — No heavy animations, optimised images

---

## Design Tokens

### Colours

```typescript
// lib/theme.ts

export const colors = {
  // Primary
  black: "#0C0C0C",        // Headers, buttons, text
  warmWhite: "#FAF9F7",    // Page backgrounds
  paperWhite: "#FFFFFF",   // Cards, inputs

  // Neutral
  slate: "#2E2E2E",        // Body text
  steel: "#5A5A5A",        // Secondary text, captions
  silver: "#E8E6E3",       // Borders, dividers

  // Accent
  blue: "#6B8EA3",         // Links, interactive
  sage: "#9BA88A",         // Success, positive

  // Semantic
  error: "#D64545",
} as const;
```

### Tailwind Config

```javascript
// tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bom: {
          black: "#0C0C0C",
          "warm-white": "#FAF9F7",
          "paper-white": "#FFFFFF",
          slate: "#2E2E2E",
          steel: "#5A5A5A",
          silver: "#E8E6E3",
          blue: "#6B8EA3",
          sage: "#9BA88A",
          error: "#D64545",
        },
      },
      fontFamily: {
        heading: ["var(--font-michroma)", "sans-serif"],
        body: ["var(--font-inter)", "sans-serif"],
      },
      spacing: {
        "18": "4.5rem",   // 72px
        "22": "5.5rem",   // 88px
      },
      maxWidth: {
        prose: "720px",
        content: "1200px",
      },
      borderRadius: {
        DEFAULT: "6px",
        lg: "8px",
      },
    },
  },
  plugins: [],
};

export default config;
```

### Typography Scale

| Element | Desktop | Mobile | Weight | Font |
|---------|---------|--------|--------|------|
| H1 | 48px | 36px | 500 | Michroma |
| H2 | 32px | 28px | 500 | Michroma |
| H3 | 24px | 20px | 500 | Michroma |
| Body | 18px | 16px | 400 | Inter |
| Body Small | 14px | 14px | 400 | Inter |
| Caption | 12px | 12px | 500 | Inter |

### Spacing Scale

Base unit: 8px

| Token | Value | Tailwind | Usage |
|-------|-------|----------|-------|
| xs | 8px | `p-2` | Icon gaps |
| sm | 16px | `p-4` | Element padding |
| md | 24px | `p-6` | Card padding |
| lg | 32px | `p-8` | Section gaps |
| xl | 48px | `p-12` | Content blocks |
| 2xl | 64px | `p-16` | Section padding (mobile) |
| 3xl | 96px | `p-24` | Section padding (desktop) |

---

## File Structure

```
website/
├── app/
│   ├── layout.tsx              # Root layout, fonts, metadata
│   ├── page.tsx                # Homepage (all sections)
│   ├── globals.css             # Tailwind imports, base styles
│   ├── voorbeelden/
│   │   └── page.tsx            # Examples page (Dutch URL)
│   ├── prijzen/
│   │   └── page.tsx            # Pricing page (Dutch URL)
│   ├── over-ons/
│   │   └── page.tsx            # About page (Dutch URL)
│   ├── contact/
│   │   └── page.tsx            # Contact page
│   ├── starten/
│   │   └── page.tsx            # Get started / intake form
│   └── api/
│       └── lead/
│           └── route.ts        # Lead capture endpoint
├── components/
│   ├── ui/
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── badge.tsx
│   │   └── section.tsx
│   ├── layout/
│   │   ├── header.tsx
│   │   ├── footer.tsx
│   │   ├── mobile-menu.tsx
│   │   └── container.tsx
│   ├── sections/
│   │   ├── hero.tsx
│   │   ├── why-bom.tsx
│   │   ├── how-it-works.tsx
│   │   ├── packages.tsx
│   │   ├── examples.tsx
│   │   ├── about.tsx
│   │   └── final-cta.tsx
│   ├── intake-form.tsx
│   ├── video-grid.tsx
│   ├── package-card.tsx
│   ├── step-card.tsx
│   └── feature-item.tsx
├── lib/
│   ├── theme.ts                # Design tokens
│   ├── utils.ts                # cn() helper, etc.
│   └── metadata.ts             # SEO defaults
├── public/
│   ├── images/
│   │   ├── logo.svg
│   │   ├── logo-white.svg
│   │   ├── monogram.svg
│   │   └── examples/           # Video thumbnails
│   ├── fonts/                  # If self-hosting
│   └── og-image.png            # Social share image
└── types/
    └── index.ts
```

---

## Task Queue

### Phase 0 (Foundation)

- [ ] Next.js 14 scaffold with App Router
- [ ] Tailwind config with design tokens
- [ ] `app/layout.tsx` — Root with Michroma + Inter fonts
- [ ] `app/globals.css` — Base styles, Tailwind layers
- [ ] `lib/utils.ts` — cn() helper (clsx + tailwind-merge)
- [ ] `components/ui/button.tsx` — Primary, secondary, text variants
- [ ] `components/ui/section.tsx` — Section wrapper with background options
- [ ] `components/layout/container.tsx` — Max-width container

### Phase 1 (Homepage)

- [ ] `components/layout/header.tsx` — Logo, nav, mobile menu
- [ ] `components/layout/footer.tsx` — Links, copyright
- [ ] `components/sections/hero.tsx` — Headline, subhead, CTA, input
- [ ] `components/sections/why-bom.tsx` — 6 value props
- [ ] `components/sections/how-it-works.tsx` — 4 steps
- [ ] `components/sections/packages.tsx` — 3 package cards
- [ ] `components/sections/examples.tsx` — Video grid (placeholder)
- [ ] `components/sections/about.tsx` — Jeroen intro
- [ ] `components/sections/final-cta.tsx` — Closing CTA
- [ ] `app/page.tsx` — Compose all sections

### Phase 2 (Subpages)

- [ ] `app/voorbeelden/page.tsx` — Full examples gallery
- [ ] `app/prijzen/page.tsx` — Detailed pricing
- [ ] `app/over-ons/page.tsx` — Extended about
- [ ] `app/contact/page.tsx` — Contact form
- [ ] `app/starten/page.tsx` — Intake form (Tally embed or custom)

### Phase 3 (Polish)

- [ ] SEO metadata for all pages
- [ ] Open Graph images
- [ ] Favicon set (monogram)
- [ ] 404 page
- [ ] Loading states
- [ ] Scroll animations (subtle fade-in only)
- [ ] Mobile menu animation
- [ ] Performance audit (Core Web Vitals)

---

## Page Specifications

### Homepage Structure

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER (sticky)                                             │
│ Logo          Nav: Voorbeelden  Prijzen  Over ons  [Start]  │
├─────────────────────────────────────────────────────────────┤
│ HERO (black background)                                     │
│                                                             │
│     Social media that actually gets done.                   │
│                                                             │
│     Professional short-form videos, delivered weekly.       │
│     We handle the ideas, scripts, editing, and captions.    │
│                                                             │
│     [========================] [Get Started]                │
│      yourwebsite.nl or @yourbusiness                        │
│                                                             │
│     Ready in 3 minutes. No call required.                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ WHY BOM (warm white background)                             │
│                                                             │
│     Better content. Less stress. More customers.            │
│                                                             │
│     ┌─────────┐  ┌─────────┐  ┌─────────┐                  │
│     │ Weekly  │  │ We do   │  │ No      │                  │
│     │ videos  │  │ the     │  │ meetings│                  │
│     │         │  │ hard    │  │         │                  │
│     │         │  │ part    │  │         │                  │
│     └─────────┘  └─────────┘  └─────────┘                  │
│     ┌─────────┐  ┌─────────┐  ┌─────────┐                  │
│     │ Fast    │  │ Your    │  │ Fixed   │                  │
│     │ delivery│  │ language│  │ pricing │                  │
│     └─────────┘  └─────────┘  └─────────┘                  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ HOW IT WORKS (white background)                             │
│                                                             │
│     From brief to first videos in under a week.             │
│                                                             │
│     1 ──────── 2 ──────── 3 ──────── 4                     │
│     Tell us   We build   Receive    Monthly                 │
│     about     your       ready-to-  check-in                │
│     your      content    post                               │
│     business  plan       videos                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ PACKAGES (warm white background)                            │
│                                                             │
│   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│   │  Kickstart   │ │   Growth     │ │    Pro       │       │
│   │  €349/mo     │ │   €649/mo    │ │   €1,250/mo  │       │
│   │              │ │              │ │              │       │
│   │  • 4 videos  │ │  • 8 videos  │ │  • 12-16     │       │
│   │  • Captions  │ │  • 3 platforms│ │  • Full      │       │
│   │  • Monthly   │ │  • Bi-weekly │ │    calendar  │       │
│   │              │ │              │ │              │       │
│   │  [Choose]    │ │  [Choose]    │ │  [Choose]    │       │
│   └──────────────┘ └──────────────┘ └──────────────┘       │
│                                                             │
│           No lock-in. Cancel anytime.                       │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ EXAMPLES (white background)                                 │
│                                                             │
│     Short-form videos for gyms, salons, cafés...            │
│                                                             │
│     ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │
│     │ ▶   │ │ ▶   │ │ ▶   │ │ ▶   │ │ ▶   │ │ ▶   │       │
│     └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘       │
│                                                             │
│                    [See all examples]                       │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ ABOUT (warm white background)                               │
│                                                             │
│     [Photo]    Hi, I'm Jeroen.                              │
│                                                             │
│                I started BOM Studios because I kept         │
│                seeing the same thing: good businesses,      │
│                invisible online...                          │
│                                                             │
│                Based in Amsterdam.                          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ FINAL CTA (black background)                                │
│                                                             │
│     Ready to stop overthinking social media?                │
│                                                             │
│     [========================] [Get Started]                │
│                                                             │
│     Or: Book a 10-minute intro call                         │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ FOOTER (black background)                                   │
│                                                             │
│     © BOM Studios                                           │
│     Professional social media content for businesses        │
│                                                             │
│     Instagram · Email · Terms                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Section Background Rhythm

| Section | Background | Text Colour |
|---------|------------|-------------|
| Header | Transparent/White | Black |
| Hero | Black (#0C0C0C) | White |
| Why BOM | Warm White (#FAF9F7) | Black |
| How It Works | White (#FFFFFF) | Black |
| Packages | Warm White (#FAF9F7) | Black |
| Examples | White (#FFFFFF) | Black |
| About | Warm White (#FAF9F7) | Black |
| Final CTA | Black (#0C0C0C) | White |
| Footer | Black (#0C0C0C) | White/Steel |

---

## Component Patterns

### Button

```tsx
// components/ui/button.tsx
import { cn } from "@/lib/utils";
import { forwardRef } from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "text" | "primary-inverted";
  size?: "sm" | "md" | "lg";
  asChild?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = "primary", size = "md", className, children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center font-body font-medium rounded transition-colors",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-bom-black focus-visible:ring-offset-2",
          "disabled:opacity-50 disabled:pointer-events-none",
          {
            // Variants
            "bg-bom-black text-white hover:bg-bom-slate": variant === "primary",
            "bg-white text-bom-black hover:bg-bom-silver": variant === "primary-inverted",
            "border border-bom-black text-bom-black hover:bg-bom-black hover:text-white":
              variant === "secondary",
            "text-bom-blue underline underline-offset-4 hover:text-bom-black":
              variant === "text",
          },
          {
            // Sizes
            "px-4 py-2 text-sm": size === "sm",
            "px-6 py-3 text-base": size === "md",
            "px-8 py-4 text-lg": size === "lg",
          },
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";
```

### Section Wrapper

```tsx
// components/ui/section.tsx
import { cn } from "@/lib/utils";

interface SectionProps {
  children: React.ReactNode;
  background?: "black" | "white" | "warm-white";
  className?: string;
  id?: string;
}

export function Section({
  children,
  background = "white",
  className,
  id,
}: SectionProps) {
  return (
    <section
      id={id}
      className={cn(
        "py-16 md:py-24",
        {
          "bg-bom-black text-white": background === "black",
          "bg-white text-bom-black": background === "white",
          "bg-bom-warm-white text-bom-black": background === "warm-white",
        },
        className
      )}
    >
      {children}
    </section>
  );
}
```

### Container

```tsx
// components/layout/container.tsx
import { cn } from "@/lib/utils";

interface ContainerProps {
  children: React.ReactNode;
  className?: string;
  narrow?: boolean;
}

export function Container({ children, className, narrow }: ContainerProps) {
  return (
    <div
      className={cn(
        "mx-auto px-4 md:px-12",
        narrow ? "max-w-prose" : "max-w-content",
        className
      )}
    >
      {children}
    </div>
  );
}
```

### Header

```tsx
// components/layout/header.tsx
"use client";

import Link from "next/link";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Container } from "@/components/layout/container";
import { MobileMenu } from "@/components/layout/mobile-menu";

const navItems = [
  { label: "Voorbeelden", href: "/voorbeelden" },
  { label: "Prijzen", href: "/prijzen" },
  { label: "Over ons", href: "/over-ons" },
];

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-bom-silver">
      <Container>
        <nav className="flex items-center justify-between h-16 md:h-20">
          {/* Logo */}
          <Link href="/" className="flex items-center">
            <img
              src="/images/logo.svg"
              alt="BOM Studios"
              className="h-6 md:h-8"
            />
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-8">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="text-bom-slate hover:text-bom-black transition-colors font-body"
              >
                {item.label}
              </Link>
            ))}
            <Button asChild>
              <Link href="/starten">Start</Link>
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2"
            onClick={() => setMobileMenuOpen(true)}
            aria-label="Open menu"
          >
            <Menu size={24} />
          </button>
        </nav>
      </Container>

      {/* Mobile Menu */}
      <MobileMenu
        open={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
        items={navItems}
      />
    </header>
  );
}
```

### Hero Section

```tsx
// components/sections/hero.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight } from "lucide-react";
import { Section } from "@/components/ui/section";
import { Container } from "@/components/layout/container";
import { Button } from "@/components/ui/button";

export function Hero() {
  const [input, setInput] = useState("");
  const router = useRouter();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    router.push(`/starten?ref=${encodeURIComponent(input)}`);
  }

  return (
    <Section background="black" className="py-20 md:py-32">
      <Container className="text-center">
        {/* Headline */}
        <h1 className="font-heading text-4xl md:text-5xl lg:text-6xl text-white mb-6">
          Social media that actually gets done.
        </h1>

        {/* Subheadline */}
        <p className="font-body text-lg md:text-xl text-bom-silver max-w-2xl mx-auto mb-10">
          Professional short-form videos, delivered weekly.
          <br className="hidden md:block" />
          We handle the ideas, scripts, editing, and captions — you post and grow.
        </p>

        {/* CTA Form */}
        <form
          onSubmit={handleSubmit}
          className="flex flex-col sm:flex-row gap-3 max-w-lg mx-auto mb-6"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="yourwebsite.nl or @yourbusiness"
            className="flex-1 px-4 py-3 rounded bg-white text-bom-black placeholder:text-bom-steel font-body"
          />
          <Button type="submit" variant="primary-inverted" className="gap-2">
            Get Started
            <ArrowRight size={18} />
          </Button>
        </form>

        {/* Microcopy */}
        <p className="text-sm text-bom-steel">
          Ready in 3 minutes. No call required.
        </p>
      </Container>
    </Section>
  );
}
```

### Package Card

```tsx
// components/package-card.tsx
import { Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface PackageCardProps {
  name: string;
  price: string;
  description: string;
  features: string[];
  highlighted?: boolean;
}

export function PackageCard({
  name,
  price,
  description,
  features,
  highlighted,
}: PackageCardProps) {
  return (
    <div
      className={cn(
        "flex flex-col p-6 md:p-8 rounded-lg border",
        highlighted
          ? "border-bom-black bg-white shadow-lg"
          : "border-bom-silver bg-bom-paper-white"
      )}
    >
      {/* Header */}
      <div className="mb-6">
        <h3 className="font-heading text-xl md:text-2xl mb-2">{name}</h3>
        <p className="font-heading text-3xl md:text-4xl mb-2">{price}</p>
        <p className="text-sm text-bom-steel">{description}</p>
      </div>

      {/* Features */}
      <ul className="flex-1 space-y-3 mb-8">
        {features.map((feature, i) => (
          <li key={i} className="flex items-start gap-3">
            <Check size={18} className="text-bom-sage mt-0.5 shrink-0" />
            <span className="text-bom-slate">{feature}</span>
          </li>
        ))}
      </ul>

      {/* CTA */}
      <Button
        variant={highlighted ? "primary" : "secondary"}
        className="w-full"
      >
        Kies {name}
      </Button>
    </div>
  );
}
```

### Step Card (How It Works)

```tsx
// components/step-card.tsx
interface StepCardProps {
  number: number;
  title: string;
  description: string;
}

export function StepCard({ number, title, description }: StepCardProps) {
  return (
    <div className="text-center md:text-left">
      {/* Step Number */}
      <div className="inline-flex items-center justify-center w-10 h-10 rounded-full bg-bom-black text-white font-heading text-lg mb-4">
        {number}
      </div>

      {/* Content */}
      <h3 className="font-heading text-lg md:text-xl mb-2">{title}</h3>
      <p className="text-bom-steel text-sm md:text-base">{description}</p>
    </div>
  );
}
```

### Feature Item (Why BOM)

```tsx
// components/feature-item.tsx
import { LucideIcon } from "lucide-react";

interface FeatureItemProps {
  icon: LucideIcon;
  title: string;
  description: string;
}

export function FeatureItem({ icon: Icon, title, description }: FeatureItemProps) {
  return (
    <div className="text-center p-6">
      <div className="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-bom-paper-white border border-bom-silver mb-4">
        <Icon size={24} className="text-bom-black" strokeWidth={1.5} />
      </div>
      <h3 className="font-body font-medium text-lg mb-2">{title}</h3>
      <p className="text-bom-steel text-sm">{description}</p>
    </div>
  );
}
```

---

## Root Layout

```tsx
// app/layout.tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import localFont from "next/font/local";
import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const michroma = localFont({
  src: "../public/fonts/Michroma-Regular.ttf",
  variable: "--font-michroma",
});

export const metadata: Metadata = {
  title: "BOM Studios — Social media that actually gets done",
  description:
    "Professional short-form videos, delivered weekly. We handle the ideas, scripts, editing, and captions — you post and grow.",
  openGraph: {
    title: "BOM Studios — Social media that actually gets done",
    description:
      "Professional short-form videos, delivered weekly. We handle the ideas, scripts, editing, and captions.",
    url: "https://bomstudios.nl",
    siteName: "BOM Studios",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
      },
    ],
    locale: "nl_NL",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "BOM Studios — Social media that actually gets done",
    description: "Professional short-form videos, delivered weekly.",
    images: ["/og-image.png"],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="nl" className={`${inter.variable} ${michroma.variable}`}>
      <body className="font-body text-bom-black bg-bom-warm-white antialiased">
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
```

---

## Global Styles

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    scroll-behavior: smooth;
  }

  body {
    @apply text-bom-slate;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    @apply font-heading text-bom-black;
  }

  p {
    @apply leading-relaxed;
  }

  /* Focus styles */
  :focus-visible {
    @apply outline-none ring-2 ring-bom-black ring-offset-2;
  }
}

@layer components {
  /* Prose for long-form content */
  .prose {
    @apply max-w-prose;
  }

  .prose p {
    @apply mb-4;
  }

  .prose h2 {
    @apply text-2xl mt-8 mb-4;
  }

  .prose h3 {
    @apply text-xl mt-6 mb-3;
  }

  .prose ul {
    @apply list-disc list-inside mb-4 space-y-2;
  }

  .prose a {
    @apply text-bom-blue underline hover:text-bom-black;
  }
}

@layer utilities {
  /* Fade-in animation for scroll */
  .fade-in {
    animation: fadeIn 0.5s ease-out forwards;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(16px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
}
```

---

## Utils

```typescript
// lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

---

## SEO & Metadata

```typescript
// lib/metadata.ts
import { Metadata } from "next";

const siteConfig = {
  name: "BOM Studios",
  description:
    "Professional short-form videos, delivered weekly. We handle the ideas, scripts, editing, and captions — you post and grow.",
  url: "https://bomstudios.nl",
  ogImage: "/og-image.png",
  locale: "nl_NL",
};

export function generateMetadata({
  title,
  description,
  path = "",
}: {
  title?: string;
  description?: string;
  path?: string;
}): Metadata {
  const pageTitle = title
    ? `${title} — ${siteConfig.name}`
    : siteConfig.name;
  const pageDescription = description || siteConfig.description;
  const url = `${siteConfig.url}${path}`;

  return {
    title: pageTitle,
    description: pageDescription,
    openGraph: {
      title: pageTitle,
      description: pageDescription,
      url,
      siteName: siteConfig.name,
      images: [{ url: siteConfig.ogImage, width: 1200, height: 630 }],
      locale: siteConfig.locale,
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title: pageTitle,
      description: pageDescription,
      images: [siteConfig.ogImage],
    },
    alternates: {
      canonical: url,
    },
  };
}
```

---

## Animation Guidelines

**Allowed:**
- Fade-in on scroll (opacity 0→1, translateY 16px→0)
- Button hover transitions (150ms ease)
- Form focus transitions (150ms ease)
- Mobile menu slide (200ms ease-out)

**Not allowed:**
- Bouncing or elastic
- Parallax scrolling
- Auto-playing video backgrounds
- Sliding from sides
- Anything that delays content visibility

```tsx
// Example: Intersection Observer for fade-in
"use client";

import { useEffect, useRef, useState } from "react";

export function useFadeIn() {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, []);

  return { ref, isVisible };
}
```

---

## Accessibility

- All images have alt text
- Colour contrast meets WCAG AA (4.5:1 for text)
- Focus states visible on all interactive elements
- Skip-to-content link (hidden until focused)
- Semantic HTML (header, main, footer, nav, section)
- Mobile menu has proper focus trap
- Form inputs have associated labels

---

## Performance Targets

| Metric | Target |
|--------|--------|
| LCP | < 2.5s |
| FID | < 100ms |
| CLS | < 0.1 |
| Lighthouse Performance | > 90 |

**Optimisations:**
- Next.js Image component for all images
- Font subsetting (Latin only)
- Lazy load below-fold images
- Minimal JavaScript (no heavy libraries)
- Static generation where possible

---

## Testing

```bash
# Dev server
cd website && npm run dev

# Type check
cd website && npm run type-check

# Lint
cd website && npm run lint

# Build
cd website && npm run build

# Lighthouse audit
npx lighthouse https://localhost:3000 --view
```

---

## Deployment

**Vercel (recommended):**

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd website && vercel
```

**Environment variables (Vercel dashboard):**
- `NEXT_PUBLIC_SITE_URL=https://bomstudios.nl`

---

## Handoff Points

- **To Portal Agent:** "Client Login" link in header/footer → portal.bomstudios.nl
- **To API Agent:** Lead capture form → POST /api/lead or Tally webhook
- **Independent:** Marketing site operates standalone, no backend dependencies

---

## When Stuck

1. Check Next.js App Router docs: https://nextjs.org/docs/app
2. Check Tailwind docs: https://tailwindcss.com/docs
3. Check `/docs/bom-studios-design-system.md` for visual specs
4. Check `/docs/bom-studios-brand-kit.md` for tone/voice
5. Check `/docs/bom-studios-website-copy-improved.md` for exact copy

---

## Copy Reference

All website copy is defined in `/docs/bom-studios-website-copy-improved.md`. Use exact wording — don't improvise headlines or CTAs.

Key copy:
- **Hero headline:** "Social media that actually gets done."
- **Hero subhead:** "Professional short-form videos, delivered weekly. We handle the ideas, scripts, editing, and captions — you post and grow."
- **CTA:** "Get Started"
- **Microcopy:** "Ready in 3 minutes. No call required."
- **Closing CTA:** "Ready to stop overthinking social media?"

---

*End of Website Agent spec.*
