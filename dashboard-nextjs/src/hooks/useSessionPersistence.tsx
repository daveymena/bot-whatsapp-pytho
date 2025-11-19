'use client'

import { useEffect } from 'react'

export function useSessionPersistence() {
  useEffect(() => {
    // Mantener sesión activa con ping cada 5 minutos
    const interval = setInterval(async () => {
      try {
        await fetch('/api/auth/ping', { method: 'POST' })
      } catch (error) {
        console.error('Error keeping session alive:', error)
      }
    }, 5 * 60 * 1000)

    return () => clearInterval(interval)
  }, [])
}
