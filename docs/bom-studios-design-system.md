# BOM Studios — Design System

Reference implementation for web properties.

---

## 1. Spacing Scale

Base unit: 8px

| Token | Value | Usage |
|-------|-------|-------|
| `xs` | 8px | Icon gaps, inline spacing |
| `sm` | 16px | Element padding, small gaps |
| `md` | 24px | Card padding, form spacing |
| `lg` | 32px | Section internal spacing |
| `xl` | 48px | Between content blocks |
| `2xl` | 64px | Section padding (mobile) |
| `3xl` | 96px | Section padding (desktop) |

---

## 2. Grid

- 12 columns  
- Max container width: 1200px  
- Gutter: 24px  
- Margin (mobile): 16px  
- Margin (desktop): 48px  

**Breakpoints:**

| Name | Width |
|------|-------|
| Mobile | < 640px |
| Tablet | 640–1024px |
| Desktop | > 1024px |

---

## 3. Typography Scale

| Element | Size | Weight | Line Height | Font |
|---------|------|--------|-------------|------|
| H1 | 48px / 36px mobile | 500 | 1.1 | Michroma |
| H2 | 32px / 28px mobile | 500 | 1.2 | Michroma |
| H3 | 24px / 20px mobile | 500 | 1.3 | Michroma |
| Body | 18px / 16px mobile | 400 | 1.5 | Inter |
| Body Small | 14px | 400 | 1.5 | Inter |
| Caption | 12px | 500 | 1.4 | Inter |

**Colour usage:**
- H1, H2, H3: BOM Black (#0C0C0C)  
- Body: Slate Grey (#2E2E2E)  
- Caption, secondary: Steel Grey (#5A5A5A)

**Background default:** Warm White (#FAF9F7)  

---

## 4. Buttons

### Primary

```
background: #0C0C0C
color: #FFFFFF
padding: 16px 32px
border-radius: 6px
font: Inter 16px Medium
```

**States:**
- Hover: background #2E2E2E  
- Active: background #000000  
- Disabled: background #E8E6E3, color #5A5A5A  

### Secondary

```
background: transparent
color: #0C0C0C
border: 1px solid #0C0C0C
padding: 16px 32px
border-radius: 6px
font: Inter 16px Medium
```

**States:**
- Hover: background #0C0C0C, color #FFFFFF  

### Text Link

```
color: #6B8EA3
text-decoration: underline
```

**States:**
- Hover: color #0C0C0C  

---

## 5. Form Elements

### Text Input

```
background: #FFFFFF
border: 1px solid #E8E6E3
border-radius: 6px
padding: 16px
font: Inter 16px
color: #0C0C0C
```

**States:**
- Focus: border-color #0C0C0C  
- Success: border-color #9BA88A  
- Error: border-color #D64545  
- Disabled: background #F5F5F5  

### Label

```
font: Inter 14px Medium
color: #2E2E2E
margin-bottom: 8px
```

### Helper Text

```
font: Inter 14px
color: #5A5A5A
margin-top: 8px
```

---

## 6. Cards

```
background: #FFFFFF
border: 1px solid #E8E6E3
border-radius: 8px
padding: 24px
```

**Variants:**
- Elevated: add `box-shadow: 0 2px 8px rgba(0,0,0,0.06)`  
- Interactive: on hover, `border-color: #0C0C0C`  

---

## 7. Section Patterns

### Standard Section

```
padding: 96px 0 (desktop)
padding: 64px 0 (mobile)
```

### Section with Background

Alternate between:
- Warm White (#FAF9F7)  
- White (#FFFFFF)  
- Black (#0C0C0C) with white text  

### Content Width

- Prose blocks: max-width 720px  
- Full sections: max-width 1200px  

---

## 8. Page Structure

```
Hero
↓
Why BOM Studios (value props)
↓
How It Works (4 steps)
↓
Packages
↓
Examples
↓
About
↓
Final CTA
↓
Footer
```

**Colour rhythm:**
- Hero: Black background  
- Why: Warm White  
- How It Works: White  
- Packages: Warm White  
- Examples: White  
- About: Warm White  
- Final CTA: Black background  
- Footer: Black background  

---

## 9. Icons

**Library:** [Lucide React](https://lucide.dev/)

**Why:** Thin outline style, 1.5px stroke default, geometric, MIT licensed, good React support.

**Usage:**
```jsx
import { Check, ArrowRight, Menu } from 'lucide-react'

<Check size={24} strokeWidth={1.5} />
```

**Rules:**
- Size: 20–24px for inline, 32px for feature icons  
- Stroke width: 1.5px (default)  
- Colour: inherit from text, or Stone Blue (#6B8EA3) for interactive, Sage (#9BA88A) for success  
- Don't mix with other icon packs  

---

## 10. Animation

**Principles:**
- Subtle, not flashy  
- Duration: 150–300ms  
- Easing: ease-out for entrances, ease-in-out for interactions  

**Allowed:**
- Fade in on scroll (opacity 0→1, translateY 16px→0)  
- Button hover transitions  
- Form focus transitions  

**Not allowed:**
- Bouncing  
- Sliding from sides  
- Parallax  
- Auto-playing video backgrounds  

---

## 11. Responsive Behaviour

| Element | Desktop | Mobile |
|---------|---------|--------|
| Hero headline | 48px | 36px |
| Section padding | 96px | 64px |
| Grid columns | 12 | 4 |
| Cards | 3-column grid | Stack |
| Navigation | Inline links | Hamburger |

---

*End of Design System.*
