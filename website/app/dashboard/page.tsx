'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useAuth } from '@/lib/auth-context'
import { useLanguage } from '@/lib/language-context'
import { FolderOpen, Video, Clock, CheckCircle } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || ''

interface Stats {
  totalProjects: number
  totalVideos: number
  pendingVideos: number
  approvedVideos: number
}

export default function DashboardPage() {
  const { token } = useAuth()
  const { language } = useLanguage()
  const [stats, setStats] = useState<Stats>({
    totalProjects: 0,
    totalVideos: 0,
    pendingVideos: 0,
    approvedVideos: 0,
  })
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (token) {
      fetchStats()
    }
  }, [token])

  async function fetchStats() {
    try {
      const [projectsRes, videosRes] = await Promise.all([
        fetch(`${API_URL}/api/projects`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
        fetch(`${API_URL}/api/videos`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ])

      if (projectsRes.ok && videosRes.ok) {
        const projects = await projectsRes.json()
        const videos = await videosRes.json()

        setStats({
          totalProjects: projects.length,
          totalVideos: videos.length,
          pendingVideos: videos.filter((v: any) => v.status === 'pending_review' || v.status === 'pending_client').length,
          approvedVideos: videos.filter((v: any) => v.status === 'approved').length,
        })
      }
    } catch {
      // API not available
    } finally {
      setIsLoading(false)
    }
  }

  const content = {
    en: {
      welcome: 'Welcome back',
      overview: 'Here\'s what\'s happening with your videos.',
      projects: 'Projects',
      videos: 'Total Videos',
      pending: 'Pending Review',
      approved: 'Approved',
      viewAll: 'View all',
      noData: 'No data yet. Submit an intake form to get started!',
    },
    nl: {
      welcome: 'Welkom terug',
      overview: 'Dit is de status van je video\'s.',
      projects: 'Projecten',
      videos: 'Totaal Video\'s',
      pending: 'Wachtend op Review',
      approved: 'Goedgekeurd',
      viewAll: 'Bekijk alles',
      noData: 'Nog geen data. Vul het intake formulier in om te beginnen!',
    },
  }

  const c = content[language]

  const statCards = [
    { label: c.projects, value: stats.totalProjects, icon: FolderOpen, color: 'bg-blue-100 text-blue-600', href: '/dashboard/projects' },
    { label: c.videos, value: stats.totalVideos, icon: Video, color: 'bg-purple-100 text-purple-600', href: '/dashboard/videos' },
    { label: c.pending, value: stats.pendingVideos, icon: Clock, color: 'bg-yellow-100 text-yellow-600', href: '/dashboard/videos?status=pending' },
    { label: c.approved, value: stats.approvedVideos, icon: CheckCircle, color: 'bg-green-100 text-green-600', href: '/dashboard/videos?status=approved' },
  ]

  return (
    <div>
      <div className="mb-8">
        <h1 className="font-heading text-2xl md:text-3xl text-bom-black mb-2">
          {c.welcome}
        </h1>
        <p className="text-bom-graphite">{c.overview}</p>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-white rounded-lg border border-bom-silver p-6 animate-pulse">
              <div className="h-10 w-10 bg-bom-silver rounded mb-4"></div>
              <div className="h-8 w-16 bg-bom-silver rounded mb-2"></div>
              <div className="h-4 w-24 bg-bom-silver rounded"></div>
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {statCards.map((stat) => (
            <Link
              key={stat.label}
              href={stat.href}
              className="bg-white rounded-lg border border-bom-silver p-6 hover:border-bom-black transition-colors"
            >
              <div className={`w-10 h-10 rounded-lg ${stat.color} flex items-center justify-center mb-4`}>
                <stat.icon className="w-5 h-5" />
              </div>
              <p className="text-3xl font-bold text-bom-black mb-1">{stat.value}</p>
              <p className="text-sm text-bom-graphite">{stat.label}</p>
            </Link>
          ))}
        </div>
      )}

      {!isLoading && stats.totalProjects === 0 && (
        <div className="mt-8 bg-white rounded-lg border border-bom-silver p-8 text-center">
          <p className="text-bom-graphite mb-4">{c.noData}</p>
          <Link
            href="/starten"
            className="inline-block bg-bom-black text-white px-6 py-3 rounded hover:bg-bom-graphite transition-colors"
          >
            {language === 'nl' ? 'Start nu' : 'Get started'}
          </Link>
        </div>
      )}
    </div>
  )
}
