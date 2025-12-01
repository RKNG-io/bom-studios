'use client'

import { useState, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import { useAuth } from '@/lib/auth-context'
import { useLanguage } from '@/lib/language-context'
import { Video, Play, CheckCircle, XCircle, Clock, Download, ExternalLink, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'

const API_URL = process.env.NEXT_PUBLIC_API_URL || ''

interface VideoItem {
  id: string
  title: string
  status: string
  video_url: string | null
  thumbnail_url: string | null
  duration: number
  video_style: string
  project_id: string
  project_name: string
  created_at: string
}

export default function VideosPage() {
  const { token } = useAuth()
  const { language } = useLanguage()
  const searchParams = useSearchParams()
  const [videos, setVideos] = useState<VideoItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState<string | null>(null)
  const [selectedVideo, setSelectedVideo] = useState<VideoItem | null>(null)

  const statusFilter = searchParams.get('status')
  const projectFilter = searchParams.get('project')

  useEffect(() => {
    if (token) {
      fetchVideos()
    }
  }, [token])

  async function fetchVideos() {
    try {
      let url = `${API_URL}/api/videos`
      if (projectFilter) {
        url += `?project_id=${projectFilter}`
      }
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (res.ok) {
        const data = await res.json()
        setVideos(data)
      }
    } catch {
      // API not available
    } finally {
      setIsLoading(false)
    }
  }

  async function handleApprove(videoId: string) {
    setActionLoading(videoId)
    try {
      const res = await fetch(`${API_URL}/api/videos/${videoId}/approve`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      })
      if (res.ok) {
        setVideos(videos.map((v) =>
          v.id === videoId ? { ...v, status: 'approved' } : v
        ))
        setSelectedVideo(null)
      }
    } catch {
      // Error
    } finally {
      setActionLoading(null)
    }
  }

  async function handleReject(videoId: string, reason?: string) {
    setActionLoading(videoId)
    try {
      const res = await fetch(`${API_URL}/api/videos/${videoId}/reject`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ reason }),
      })
      if (res.ok) {
        setVideos(videos.map((v) =>
          v.id === videoId ? { ...v, status: 'rejected' } : v
        ))
        setSelectedVideo(null)
      }
    } catch {
      // Error
    } finally {
      setActionLoading(null)
    }
  }

  const content = {
    en: {
      title: 'Videos',
      subtitle: 'Review and approve your videos',
      noVideos: 'No videos yet',
      noVideosDesc: 'Videos will appear here once they\'re generated.',
      approve: 'Approve',
      reject: 'Request Changes',
      approved: 'Approved',
      rejected: 'Changes Requested',
      pending: 'Pending Review',
      generating: 'Generating',
      download: 'Download',
      preview: 'Preview',
      close: 'Close',
      all: 'All',
      filterPending: 'Pending',
      filterApproved: 'Approved',
    },
    nl: {
      title: "Video's",
      subtitle: "Bekijk en keur je video's goed",
      noVideos: "Nog geen video's",
      noVideosDesc: "Video's verschijnen hier zodra ze zijn gegenereerd.",
      approve: 'Goedkeuren',
      reject: 'Wijzigingen aanvragen',
      approved: 'Goedgekeurd',
      rejected: 'Wijzigingen gevraagd',
      pending: 'Wacht op review',
      generating: 'Aan het genereren',
      download: 'Download',
      preview: 'Bekijken',
      close: 'Sluiten',
      all: 'Alle',
      filterPending: 'Wachtend',
      filterApproved: 'Goedgekeurd',
    },
  }

  const c = content[language]

  const statusConfig: Record<string, { label: string; color: string; icon: any }> = {
    pending_client: { label: c.pending, color: 'bg-yellow-100 text-yellow-700', icon: Clock },
    pending_review: { label: c.pending, color: 'bg-yellow-100 text-yellow-700', icon: Clock },
    approved: { label: c.approved, color: 'bg-green-100 text-green-700', icon: CheckCircle },
    rejected: { label: c.rejected, color: 'bg-red-100 text-red-700', icon: XCircle },
    generating: { label: c.generating, color: 'bg-blue-100 text-blue-700', icon: Loader2 },
  }

  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleDateString(language === 'nl' ? 'nl-NL' : 'en-US', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    })
  }

  const filteredVideos = videos.filter((v) => {
    if (statusFilter === 'pending') {
      return v.status === 'pending_client' || v.status === 'pending_review'
    }
    if (statusFilter === 'approved') {
      return v.status === 'approved'
    }
    return true
  })

  return (
    <div>
      <div className="mb-8">
        <h1 className="font-heading text-2xl md:text-3xl text-bom-black mb-2">
          {c.title}
        </h1>
        <p className="text-bom-graphite">{c.subtitle}</p>
      </div>

      {/* Filters */}
      <div className="flex gap-2 mb-6">
        {[
          { key: null, label: c.all },
          { key: 'pending', label: c.filterPending },
          { key: 'approved', label: c.filterApproved },
        ].map((filter) => (
          <a
            key={filter.key || 'all'}
            href={filter.key ? `/dashboard/videos?status=${filter.key}` : '/dashboard/videos'}
            className={`px-4 py-2 rounded text-sm transition-colors ${
              statusFilter === filter.key
                ? 'bg-bom-black text-white'
                : 'bg-white border border-bom-silver text-bom-graphite hover:border-bom-black'
            }`}
          >
            {filter.label}
          </a>
        ))}
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-white rounded-lg border border-bom-silver overflow-hidden animate-pulse">
              <div className="aspect-[9/16] bg-bom-silver"></div>
              <div className="p-4">
                <div className="h-5 w-32 bg-bom-silver rounded mb-2"></div>
                <div className="h-4 w-24 bg-bom-silver rounded"></div>
              </div>
            </div>
          ))}
        </div>
      ) : filteredVideos.length === 0 ? (
        <div className="bg-white rounded-lg border border-bom-silver p-8 text-center">
          <Video className="w-12 h-12 text-bom-silver mx-auto mb-4" />
          <p className="text-bom-graphite mb-2">{c.noVideos}</p>
          <p className="text-sm text-bom-steel">{c.noVideosDesc}</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredVideos.map((video) => {
            const status = statusConfig[video.status] || statusConfig.pending_client
            const StatusIcon = status.icon
            const canApprove = video.status === 'pending_client' || video.status === 'pending_review'

            return (
              <div
                key={video.id}
                className="bg-white rounded-lg border border-bom-silver overflow-hidden hover:border-bom-black transition-colors"
              >
                {/* Thumbnail / Preview */}
                <div className="aspect-[9/16] bg-bom-graphite relative group">
                  {video.thumbnail_url ? (
                    <img
                      src={video.thumbnail_url}
                      alt={video.title}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <Video className="w-12 h-12 text-bom-steel" />
                    </div>
                  )}

                  {/* Play overlay */}
                  {video.video_url && (
                    <button
                      onClick={() => setSelectedVideo(video)}
                      className="absolute inset-0 flex items-center justify-center bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center">
                        <Play className="w-8 h-8 text-bom-black ml-1" />
                      </div>
                    </button>
                  )}

                  {/* Status badge */}
                  <div className={`absolute top-3 left-3 flex items-center gap-1 text-xs px-2 py-1 rounded ${status.color}`}>
                    <StatusIcon className={`w-3 h-3 ${video.status === 'generating' ? 'animate-spin' : ''}`} />
                    {status.label}
                  </div>
                </div>

                {/* Info */}
                <div className="p-4">
                  <h3 className="font-medium text-bom-black mb-1 truncate">{video.title}</h3>
                  <p className="text-sm text-bom-graphite mb-3">
                    {video.project_name} • {formatDate(video.created_at)}
                  </p>

                  {/* Actions */}
                  {canApprove && video.video_url && (
                    <div className="flex gap-2">
                      <Button
                        onClick={() => handleApprove(video.id)}
                        disabled={actionLoading === video.id}
                        className="flex-1 text-sm"
                      >
                        {actionLoading === video.id ? (
                          <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                          <>
                            <CheckCircle className="w-4 h-4 mr-1" />
                            {c.approve}
                          </>
                        )}
                      </Button>
                      <button
                        onClick={() => handleReject(video.id)}
                        disabled={actionLoading === video.id}
                        className="px-3 py-2 border border-bom-silver rounded text-sm text-bom-graphite hover:border-bom-black transition-colors"
                      >
                        <XCircle className="w-4 h-4" />
                      </button>
                    </div>
                  )}

                  {video.status === 'approved' && video.video_url && (
                    <a
                      href={video.video_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-center gap-2 w-full px-4 py-2 bg-green-600 text-white rounded text-sm hover:bg-green-700 transition-colors"
                    >
                      <Download className="w-4 h-4" />
                      {c.download}
                    </a>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Video Preview Modal */}
      {selectedVideo && selectedVideo.video_url && (
        <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-lg w-full overflow-hidden">
            <div className="aspect-[9/16] bg-black">
              <video
                src={selectedVideo.video_url}
                controls
                autoPlay
                className="w-full h-full"
              />
            </div>
            <div className="p-4 flex items-center justify-between">
              <h3 className="font-medium text-bom-black">{selectedVideo.title}</h3>
              <div className="flex gap-2">
                {(selectedVideo.status === 'pending_client' || selectedVideo.status === 'pending_review') && (
                  <Button
                    onClick={() => handleApprove(selectedVideo.id)}
                    disabled={actionLoading === selectedVideo.id}
                  >
                    {actionLoading === selectedVideo.id ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      c.approve
                    )}
                  </Button>
                )}
                <button
                  onClick={() => setSelectedVideo(null)}
                  className="px-4 py-2 border border-bom-silver rounded hover:border-bom-black transition-colors"
                >
                  {c.close}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
