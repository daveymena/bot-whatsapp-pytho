'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function ProductsPage() {
  const router = useRouter()

  useEffect(() => {
    // Redirigir al dashboard principal con el tab de productos
    router.push('/dashboard?tab=products')
  }, [router])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <p className="text-sm text-gray-600">Redirigiendo...</p>
      </div>
    </div>
  )
}
