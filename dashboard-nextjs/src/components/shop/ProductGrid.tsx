'use client'

import { ProductCard } from './ProductCard'
import { Loader2 } from 'lucide-react'

interface ProductGridProps {
  products: any[]
  loading: boolean
  onCartUpdate: () => void
}

export function ProductGrid({ products, loading, onCartUpdate }: ProductGridProps) {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    )
  }

  if (products.length === 0) {
    return (
      <div className="text-center py-20">
        <p className="text-gray-500 text-lg">No se encontraron productos</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {products.map((product) => (
        <ProductCard 
          key={product.id} 
          product={product}
          onCartUpdate={onCartUpdate}
        />
      ))}
    </div>
  )
}
