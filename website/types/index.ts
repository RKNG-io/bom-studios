/**
 * Navigation item for header and footer menus
 */
export interface NavItem {
  label: string
  href: string
}

/**
 * Service package with pricing and features
 */
export interface Package {
  name: string
  price: string
  description: string
  features: string[]
  highlighted?: boolean
}

/**
 * Process step for the "How it works" section
 */
export interface Step {
  number: number
  title: string
  description: string
}

/**
 * Feature with icon, title, and description
 */
export interface Feature {
  icon: string
  title: string
  description: string
}
