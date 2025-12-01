# SKILL.md — Portal Agent

## Role

Build and maintain the Next.js client portal where clients log in, view their videos, approve content, and download deliverables.

---

## Scope

- `portal/` directory only
- Client authentication (magic link)
- Dashboard with project status
- Video review and approval flow
- Content calendar view (Phase 3)

**Out of scope:** Flet engine, FastAPI backend logic, n8n workflows

---

## Tech Stack

- Next.js 14 (App Router)
- TypeScript (strict)
- Tailwind CSS
- Lucide React (icons)
- React Query (data fetching)

---

## Design System Tokens

```typescript
// lib/theme.ts

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

export const spacing = {
  xs: "0.5rem",    // 8px
  sm: "1rem",      // 16px
  md: "1.5rem",    // 24px
  lg: "2rem",      // 32px
  xl: "3rem",      // 48px
  "2xl": "4rem",   // 64px
  "3xl": "6rem",   // 96px
} as const;
```

**Tailwind config extension:**

```javascript
// tailwind.config.js
module.exports = {
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
        heading: ["Michroma", "sans-serif"],
        body: ["Inter", "sans-serif"],
      },
    },
  },
};
```

---

## File Structure

```
portal/
├── app/
│   ├── layout.tsx            # Root layout with fonts
│   ├── page.tsx              # Landing → redirect to login or dashboard
│   ├── login/
│   │   └── page.tsx          # Magic link login form
│   ├── verify/
│   │   └── page.tsx          # Token verification handler
│   ├── (authenticated)/
│   │   ├── layout.tsx        # Authenticated layout with nav
│   │   ├── dashboard/
│   │   │   └── page.tsx      # Client dashboard
│   │   ├── videos/
│   │   │   ├── page.tsx      # Video list
│   │   │   └── [id]/
│   │   │       └── page.tsx  # Video detail + approval
│   │   ├── calendar/
│   │   │   └── page.tsx      # Content calendar (Phase 3)
│   │   └── settings/
│   │       └── page.tsx      # Client settings
│   └── api/
│       └── auth/
│           └── [...nextauth]/
│               └── route.ts  # Auth routes (if using NextAuth)
├── components/
│   ├── ui/
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── badge.tsx
│   │   └── modal.tsx
│   ├── layout/
│   │   ├── header.tsx
│   │   ├── sidebar.tsx
│   │   └── footer.tsx
│   ├── video-card.tsx
│   ├── video-player.tsx
│   ├── approval-form.tsx
│   └── status-badge.tsx
├── lib/
│   ├── api.ts                # API client
│   ├── auth.ts               # Auth helpers
│   ├── theme.ts              # Design tokens
│   └── utils.ts              # Helpers
├── hooks/
│   ├── use-auth.ts
│   ├── use-videos.ts
│   └── use-projects.ts
└── types/
    └── index.ts              # TypeScript types
```

---

## Task Queue

### Phase 0 (Foundation)

- [ ] Next.js scaffold with App Router
- [ ] Tailwind config with design tokens
- [ ] `app/layout.tsx` — Root with fonts (Michroma, Inter)
- [ ] `lib/api.ts` — API client setup
- [ ] `components/ui/button.tsx` — Primary, secondary variants
- [ ] `components/ui/card.tsx`
- [ ] `components/ui/input.tsx`

### Phase 1c (Auth + Basic Portal)

- [ ] `app/login/page.tsx` — Email input, magic link request
- [ ] `app/verify/page.tsx` — Token verification, redirect
- [ ] `lib/auth.ts` — Token storage, auth state
- [ ] `hooks/use-auth.ts` — Auth hook
- [ ] `app/(authenticated)/layout.tsx` — Protected layout
- [ ] `components/layout/header.tsx` — Logo, user menu
- [ ] `app/(authenticated)/dashboard/page.tsx` — Welcome, active projects

### Phase 1c (Videos)

- [ ] `types/index.ts` — Video, Project types
- [ ] `hooks/use-videos.ts` — Fetch videos
- [ ] `app/(authenticated)/videos/page.tsx` — Video list
- [ ] `components/video-card.tsx` — Thumbnail, status, actions
- [ ] `app/(authenticated)/videos/[id]/page.tsx` — Video detail
- [ ] `components/video-player.tsx` — Video preview
- [ ] `components/approval-form.tsx` — Approve/reject with note
- [ ] `components/status-badge.tsx` — Status indicator

### Phase 3 (Calendar)

- [ ] `app/(authenticated)/calendar/page.tsx` — Monthly view
- [ ] Calendar component (use a library or build simple)
- [ ] Scheduled videos display

---

## Component Patterns

### Button

```tsx
// components/ui/button.tsx
import { cn } from "@/lib/utils";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "text";
  size?: "sm" | "md" | "lg";
}

export function Button({
  variant = "primary",
  size = "md",
  className,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        "font-body rounded-md transition-colors",
        {
          "bg-bom-black text-white hover:bg-bom-slate": variant === "primary",
          "border border-bom-black text-bom-black hover:bg-bom-black hover:text-white":
            variant === "secondary",
          "text-bom-blue underline hover:text-bom-black": variant === "text",
        },
        {
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
```

### Card

```tsx
// components/ui/card.tsx
import { cn } from "@/lib/utils";

interface CardProps {
  children: React.ReactNode;
  className?: string;
  interactive?: boolean;
}

export function Card({ children, className, interactive }: CardProps) {
  return (
    <div
      className={cn(
        "bg-bom-paper-white border border-bom-silver rounded-lg p-6",
        interactive && "hover:border-bom-black transition-colors cursor-pointer",
        className
      )}
    >
      {children}
    </div>
  );
}
```

### Video Card

```tsx
// components/video-card.tsx
import { Card } from "@/components/ui/card";
import { StatusBadge } from "@/components/status-badge";
import { Video } from "@/types";

interface VideoCardProps {
  video: Video;
  onClick?: () => void;
}

export function VideoCard({ video, onClick }: VideoCardProps) {
  return (
    <Card interactive onClick={onClick}>
      <div className="aspect-[9/16] bg-bom-silver rounded-md mb-4 overflow-hidden">
        {video.thumbnail_url ? (
          <img
            src={video.thumbnail_url}
            alt={video.title}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-bom-steel">
            No preview
          </div>
        )}
      </div>
      <h3 className="font-body font-medium text-bom-black mb-2">
        {video.title}
      </h3>
      <StatusBadge status={video.status} />
    </Card>
  );
}
```

---

## API Client

```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

async function fetcher<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const token = localStorage.getItem("auth_token");

  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options?.headers,
    },
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }

  return res.json();
}

export const api = {
  // Auth
  sendMagicLink: (email: string) =>
    fetcher("/auth/magic-link", {
      method: "POST",
      body: JSON.stringify({ email }),
    }),

  verifyToken: (token: string) =>
    fetcher<{ access_token: string; client: Client }>(`/auth/verify?token=${token}`),

  // Videos
  getVideos: () => fetcher<Video[]>("/videos"),

  getVideo: (id: string) => fetcher<Video>(`/videos/${id}`),

  approveVideo: (id: string, data: { approved: boolean; note?: string }) =>
    fetcher(`/videos/${id}/approve`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  // Projects
  getProjects: () => fetcher<Project[]>("/projects"),
};
```

---

## Auth Flow

```tsx
// app/login/page.tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);

    try {
      await api.sendMagicLink(email);
      setSent(true);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  if (sent) {
    return (
      <div className="min-h-screen bg-bom-warm-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="font-heading text-2xl mb-4">Check your email</h1>
          <p className="text-bom-steel">
            We've sent a login link to {email}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-bom-warm-white flex items-center justify-center">
      <form onSubmit={handleSubmit} className="w-full max-w-sm">
        <h1 className="font-heading text-2xl mb-8 text-center">
          Client Portal
        </h1>
        <Input
          type="email"
          placeholder="your@email.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="mb-4"
        />
        <Button type="submit" disabled={loading} className="w-full">
          {loading ? "Sending..." : "Send Login Link"}
        </Button>
      </form>
    </div>
  );
}
```

```tsx
// app/verify/page.tsx
"use client";

import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { api } from "@/lib/api";

export default function VerifyPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  useEffect(() => {
    async function verify() {
      if (!token) {
        router.push("/login");
        return;
      }

      try {
        const { access_token } = await api.verifyToken(token);
        localStorage.setItem("auth_token", access_token);
        router.push("/dashboard");
      } catch (error) {
        console.error(error);
        router.push("/login");
      }
    }

    verify();
  }, [token, router]);

  return (
    <div className="min-h-screen bg-bom-warm-white flex items-center justify-center">
      <p>Verifying...</p>
    </div>
  );
}
```

---

## Approval Flow

```tsx
// components/approval-form.tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";

interface ApprovalFormProps {
  videoId: string;
  onComplete: () => void;
}

export function ApprovalForm({ videoId, onComplete }: ApprovalFormProps) {
  const [note, setNote] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleApprove() {
    setLoading(true);
    await api.approveVideo(videoId, { approved: true });
    onComplete();
  }

  async function handleReject() {
    if (!note.trim()) {
      alert("Please add a note explaining what changes you'd like.");
      return;
    }
    setLoading(true);
    await api.approveVideo(videoId, { approved: false, note });
    onComplete();
  }

  return (
    <div className="space-y-4">
      <textarea
        placeholder="Add a note (required for changes)..."
        value={note}
        onChange={(e) => setNote(e.target.value)}
        className="w-full p-4 border border-bom-silver rounded-md"
        rows={3}
      />
      <div className="flex gap-4">
        <Button onClick={handleApprove} disabled={loading}>
          Approve
        </Button>
        <Button variant="secondary" onClick={handleReject} disabled={loading}>
          Request Changes
        </Button>
      </div>
    </div>
  );
}
```

---

## Types

```typescript
// types/index.ts

export interface Client {
  id: string;
  name: string;
  email: string;
  package: "kickstart" | "growth" | "pro";
  brand_kit?: {
    logo_url?: string;
    colours?: string[];
  };
  created_at: string;
}

export interface Project {
  id: string;
  client_id: string;
  name: string;
  status: "draft" | "in_progress" | "review" | "approved" | "delivered";
  created_at: string;
}

export interface Video {
  id: string;
  project_id: string;
  title: string;
  script?: {
    hook: string;
    scenes: Array<{ text: string; duration: number }>;
    cta: string;
  };
  status: "scripting" | "generating" | "rendering" | "draft" | "approved" | "delivered";
  formats?: {
    vertical?: string;
    square?: string;
    horizontal?: string;
  };
  thumbnail_url?: string;
  cost_cents: number;
  created_at: string;
}
```

---

## Testing

```bash
# Dev server
cd portal && npm run dev

# Type check
cd portal && npm run type-check

# Lint
cd portal && npm run lint

# Build
cd portal && npm run build
```

---

## Handoff Points

- **From API Agent:** All data comes from API endpoints
- **To API Agent:** Approval actions call API endpoints
- **To Engine Agent:** Status changes visible when Engine refreshes

---

## When Stuck

1. Check Next.js App Router docs: https://nextjs.org/docs/app
2. Check `/docs/design-system.md` for visual specs
3. Check `/docs/website-copy.md` for tone/copy guidance
4. If API endpoint missing, mock the response and continue
