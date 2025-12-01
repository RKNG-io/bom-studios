"use client"

import { createContext, useContext, useState, useEffect, ReactNode } from "react"
import { useRouter } from "next/navigation"

interface User {
  id: string
  email: string
  businessName: string
}

interface AuthContextType {
  user: User | null
  token: string | null
  isLoading: boolean
  login: (token: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

const API_URL = process.env.NEXT_PUBLIC_API_URL || ""

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  // Load saved token on mount
  useEffect(() => {
    const savedToken = localStorage.getItem("bom-token")
    if (savedToken) {
      setToken(savedToken)
      fetchUser(savedToken)
    } else {
      setIsLoading(false)
    }
  }, [])

  async function fetchUser(authToken: string) {
    try {
      const res = await fetch(`${API_URL}/api/auth/me`, {
        headers: { Authorization: `Bearer ${authToken}` },
      })
      if (res.ok) {
        const data = await res.json()
        setUser(data)
      } else {
        // Token invalid, clear it
        localStorage.removeItem("bom-token")
        setToken(null)
      }
    } catch {
      // API not available, keep token for later
    } finally {
      setIsLoading(false)
    }
  }

  async function login(newToken: string) {
    localStorage.setItem("bom-token", newToken)
    setToken(newToken)
    await fetchUser(newToken)
    router.push("/dashboard")
  }

  function logout() {
    localStorage.removeItem("bom-token")
    setToken(null)
    setUser(null)
    router.push("/")
  }

  return (
    <AuthContext.Provider value={{ user, token, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
