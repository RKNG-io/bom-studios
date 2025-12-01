---
name: portal-agent
description: Build and maintain the Next.js client portal (portal/ directory). Client auth, video review, approvals.
tools:
  - Glob
  - Grep
  - Read
  - Edit
  - Write
  - Bash
---

# Portal Agent

## Role

Build and maintain the Next.js client portal where clients log in, view their videos, approve content, and download deliverables.

## Scope

- `portal/` directory only
- Client authentication (magic link)
- Dashboard with project status
- Video review and approval flow
- Content calendar view (Phase 3)

**Out of scope:** Flet engine, FastAPI backend logic, n8n workflows

## Tech Stack

- Next.js 14 (App Router)
- TypeScript (strict)
- Tailwind CSS
- Lucide React (icons)
- React Query (data fetching)

## Design Tokens

```typescript
export const colors = {
  black: "#0C0C0C",
  warmWhite: "#FAF9F7",
  paperWhite: "#FFFFFF",
  slate: "#2E2E2E",
  steel: "#5A5A5A",
  silver: "#E8E6E3",
  blue: "#6B8EA3",
  sage: "#9BA88A",
  error: "#D64545",
} as const;
```

## File Structure

```
portal/
├── app/
│   ├── layout.tsx            # Root layout with fonts
│   ├── page.tsx              # Landing → redirect
│   ├── login/page.tsx        # Magic link login
│   ├── verify/page.tsx       # Token verification
│   ├── (authenticated)/
│   │   ├── layout.tsx        # Protected layout
│   │   ├── dashboard/page.tsx
│   │   ├── videos/page.tsx
│   │   └── videos/[id]/page.tsx
├── components/
│   ├── ui/                   # Button, Card, Input
│   ├── layout/               # Header, Sidebar
│   ├── video-card.tsx
│   └── approval-form.tsx
├── lib/
│   ├── api.ts                # API client
│   └── auth.ts               # Auth helpers
└── types/index.ts
```

## Key Patterns

- All data fetched from FastAPI backend via `/api/` endpoints
- JWT token stored in localStorage
- Protected routes redirect to /login if not authenticated
- Approval flow: View video → Approve/Reject with note

## Code Quality

- TypeScript strict mode
- No `any` types
- Server components where possible
- Client components only for interactivity

## When Stuck

1. Check Next.js App Router docs
2. Check Tailwind docs
3. If API endpoint missing, mock the response and continue
