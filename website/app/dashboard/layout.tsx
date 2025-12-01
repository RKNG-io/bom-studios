'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useAuth } from '@/lib/auth-context'
import { useLanguage } from '@/lib/language-context'
import { Container } from '@/components/layout/container'
import { LayoutDashboard, FolderOpen, Video, LogOut, Loader2 } from 'lucide-react'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const { user, isLoading, logout } = useAuth()
  const { language } = useLanguage()
  const router = useRouter()
  const pathname = usePathname()

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/login')
    }
  }, [user, isLoading, router])

  if (isLoading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-bom-blue animate-spin" />
      </div>
    )
  }

  if (!user) {
    return null
  }

  const nav = {
    en: {
      overview: 'Overview',
      projects: 'Projects',
      videos: 'Videos',
      logout: 'Log out',
    },
    nl: {
      overview: 'Overzicht',
      projects: 'Projecten',
      videos: "Video's",
      logout: 'Uitloggen',
    },
  }

  const n = nav[language]

  const links = [
    { href: '/dashboard', label: n.overview, icon: LayoutDashboard },
    { href: '/dashboard/projects', label: n.projects, icon: FolderOpen },
    { href: '/dashboard/videos', label: n.videos, icon: Video },
  ]

  return (
    <div className="min-h-[60vh] bg-bom-warm-white">
      <Container>
        <div className="flex flex-col md:flex-row gap-8 py-8">
          {/* Sidebar */}
          <aside className="w-full md:w-64 flex-shrink-0">
            <div className="bg-white rounded-lg border border-bom-silver p-4">
              {/* User info */}
              <div className="pb-4 mb-4 border-b border-bom-silver">
                <p className="font-medium text-bom-black truncate">
                  {user.businessName || user.email}
                </p>
                <p className="text-sm text-bom-steel truncate">{user.email}</p>
              </div>

              {/* Navigation */}
              <nav className="space-y-1">
                {links.map((link) => {
                  const isActive = pathname === link.href
                  return (
                    <Link
                      key={link.href}
                      href={link.href}
                      className={`flex items-center gap-3 px-3 py-2 rounded transition-colors ${
                        isActive
                          ? 'bg-bom-black text-white'
                          : 'text-bom-graphite hover:bg-bom-warm-white'
                      }`}
                    >
                      <link.icon className="w-5 h-5" />
                      {link.label}
                    </Link>
                  )
                })}
              </nav>

              {/* Logout */}
              <div className="pt-4 mt-4 border-t border-bom-silver">
                <button
                  onClick={logout}
                  className="flex items-center gap-3 px-3 py-2 w-full text-left text-bom-steel hover:text-bom-black transition-colors"
                >
                  <LogOut className="w-5 h-5" />
                  {n.logout}
                </button>
              </div>
            </div>
          </aside>

          {/* Main content */}
          <main className="flex-1 min-w-0">
            {children}
          </main>
        </div>
      </Container>
    </div>
  )
}
