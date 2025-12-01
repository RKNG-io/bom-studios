'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useAuth } from '@/lib/auth-context'
import { useLanguage } from '@/lib/language-context'
import { FolderOpen, Calendar, Video, ArrowRight } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || ''

interface Project {
  id: string
  name: string
  status: string
  video_style: string
  video_count: number
  created_at: string
}

export default function ProjectsPage() {
  const { token } = useAuth()
  const { language } = useLanguage()
  const [projects, setProjects] = useState<Project[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (token) {
      fetchProjects()
    }
  }, [token])

  async function fetchProjects() {
    try {
      const res = await fetch(`${API_URL}/api/projects`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (res.ok) {
        const data = await res.json()
        setProjects(data)
      }
    } catch {
      // API not available
    } finally {
      setIsLoading(false)
    }
  }

  const content = {
    en: {
      title: 'Projects',
      subtitle: 'All your video projects',
      noProjects: 'No projects yet',
      startProject: 'Start your first project',
      videos: 'videos',
      created: 'Created',
      viewVideos: 'View videos',
    },
    nl: {
      title: 'Projecten',
      subtitle: 'Al je video projecten',
      noProjects: 'Nog geen projecten',
      startProject: 'Start je eerste project',
      videos: "video's",
      created: 'Aangemaakt',
      viewVideos: "Bekijk video's",
    },
  }

  const c = content[language]

  const statusLabels: Record<string, { en: string; nl: string; color: string }> = {
    active: { en: 'Active', nl: 'Actief', color: 'bg-green-100 text-green-700' },
    pending: { en: 'Pending', nl: 'In behandeling', color: 'bg-yellow-100 text-yellow-700' },
    completed: { en: 'Completed', nl: 'Afgerond', color: 'bg-blue-100 text-blue-700' },
  }

  const styleLabels: Record<string, string> = {
    presenter: 'Presenter',
    product: 'Product',
    animated: 'Animated',
    voiceover: 'Voiceover',
    hybrid: 'Hybrid',
  }

  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleDateString(language === 'nl' ? 'nl-NL' : 'en-US', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    })
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="font-heading text-2xl md:text-3xl text-bom-black mb-2">
          {c.title}
        </h1>
        <p className="text-bom-graphite">{c.subtitle}</p>
      </div>

      {isLoading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-white rounded-lg border border-bom-silver p-6 animate-pulse">
              <div className="h-6 w-48 bg-bom-silver rounded mb-4"></div>
              <div className="h-4 w-32 bg-bom-silver rounded"></div>
            </div>
          ))}
        </div>
      ) : projects.length === 0 ? (
        <div className="bg-white rounded-lg border border-bom-silver p-8 text-center">
          <FolderOpen className="w-12 h-12 text-bom-silver mx-auto mb-4" />
          <p className="text-bom-graphite mb-4">{c.noProjects}</p>
          <Link
            href="/starten"
            className="inline-block bg-bom-black text-white px-6 py-3 rounded hover:bg-bom-graphite transition-colors"
          >
            {c.startProject}
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {projects.map((project) => {
            const status = statusLabels[project.status] || statusLabels.pending
            return (
              <div
                key={project.id}
                className="bg-white rounded-lg border border-bom-silver p-6 hover:border-bom-black transition-colors"
              >
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h2 className="font-medium text-lg text-bom-black">{project.name}</h2>
                      <span className={`text-xs px-2 py-1 rounded ${status.color}`}>
                        {status[language]}
                      </span>
                    </div>
                    <div className="flex flex-wrap items-center gap-4 text-sm text-bom-graphite">
                      <span className="flex items-center gap-1">
                        <Video className="w-4 h-4" />
                        {project.video_count || 0} {c.videos}
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {c.created} {formatDate(project.created_at)}
                      </span>
                      {project.video_style && (
                        <span className="bg-bom-warm-white px-2 py-1 rounded text-xs">
                          {styleLabels[project.video_style] || project.video_style}
                        </span>
                      )}
                    </div>
                  </div>
                  <Link
                    href={`/dashboard/videos?project=${project.id}`}
                    className="flex items-center gap-2 text-bom-blue hover:text-bom-black transition-colors"
                  >
                    {c.viewVideos}
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
