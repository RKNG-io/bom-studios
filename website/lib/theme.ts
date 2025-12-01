/**
 * BOM Studios Design System
 * Centralised theme constants for use in TypeScript/React components
 */

export const colors = {
  bomBlack: '#0C0C0C',
  bomWarmWhite: '#FAF9F7',
  bomPaperWhite: '#FFFFFF',
  bomSlate: '#2E2E2E',
  bomSteel: '#5A5A5A',
  bomSilver: '#E8E6E3',
  bomBlue: '#6B8EA3',
  bomSage: '#9BA88A',
  bomError: '#D64545',
} as const

export const spacing = {
  prose: '720px',
  content: '1200px',
} as const

export const fonts = {
  heading: 'var(--font-michroma)',
  body: 'var(--font-inter)',
} as const

export type ColorKey = keyof typeof colors
export type SpacingKey = keyof typeof spacing
export type FontKey = keyof typeof fonts
