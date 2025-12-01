import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'bom-black': '#0C0C0C',
        'bom-warm-white': '#FAF9F7',
        'bom-paper-white': '#FFFFFF',
        'bom-slate': '#2E2E2E',
        'bom-steel': '#5A5A5A',
        'bom-silver': '#E8E6E3',
        'bom-blue': '#6B8EA3',
        'bom-sage': '#9BA88A',
        'bom-error': '#D64545',
      },
      fontFamily: {
        heading: ['var(--font-michroma)', 'sans-serif'],
        body: ['var(--font-inter)', 'sans-serif'],
      },
      maxWidth: {
        prose: '720px',
        content: '1200px',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}

export default config
