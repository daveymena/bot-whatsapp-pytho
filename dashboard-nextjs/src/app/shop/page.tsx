'use client'

import { useState, useEffect } from 'react'
import { ShopHeader } from '@/components/shop/ShopHeader'
import { ProductGrid } from '@/components/shop/ProductGrid'
import { ShoppingCart, Search } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import Link from 'next/link'

export default function ShopPage() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [category, setCategory] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [cartCount, setCartCount] = useState(0)

  useEffect(() => {
    loadProducts()
    loadCartCount()
  }, [])

  const loadProducts = async () => {
    try {
      const response = await fetch('http://localhost:5000/admin/products')
      if (response.ok) {
        const data = await response.json()
        setProducts(data)
      }
    } catch (error) {
      console.error('Error loading products:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadCartCount = () => {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]')
    setCartCount(cart.reduce((sum: number, item: any) => sum + item.quantity, 0))
  }

  const filteredProducts = products.filter((product: any) => {
    const matchesCategory = category === 'all' || 
      (category === 'physical' && !product.is_digital && !product.is_dropshipping) ||
      (category === 'digital' && product.is_digital) ||
      (category === 'services' && product.category === 'servicios')
    
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.description?.toLowerCase().includes(searchTerm.toLowerCase())
    
    return matchesCategory && matchesSearch
  })

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <ShopHeader cartCount={cartCount} />

      {/* Search Bar */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="relative max-w-2xl mx-auto">
            <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
            <Input
              type="search"
              placeholder="Buscar productos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-6 text-lg"
            />
          </div>
        </div>
      </div>

      {/* Categories */}
      <div className="bg-red-600 text-white">
        <div className="container mx-auto px-4">
          <div className="flex gap-4 overflow-x-auto py-3">
            <Button
              variant={category === 'all' ? 'secondary' : 'ghost'}
              onClick={() => setCategory('all')}
              className={category === 'all' ? 'bg-white text-red-600' : 'text-white hover:bg-red-700'}
            >
              Todos
            </Button>
            <Button
              variant={category === 'physical' ? 'secondary' : 'ghost'}
              onClick={() => setCategory('physical')}
              className={category === 'physical' ? 'bg-white text-red-600' : 'text-white hover:bg-red-700'}
            >
              Físicos
            </Button>
            <Button
              variant={category === 'digital' ? 'secondary' : 'ghost'}
              onClick={() => setCategory('digital')}
              className={category === 'digital' ? 'bg-white text-red-600' : 'text-white hover:bg-red-700'}
            >
              Digitales
            </Button>
            <Button
              variant={category === 'services' ? 'secondary' : 'ghost'}
              onClick={() => setCategory('services')}
              className={category === 'services' ? 'bg-white text-red-600' : 'text-white hover:bg-red-700'}
            >
              Servicios
            </Button>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="container mx-auto px-4 py-8">
        <ProductGrid 
          products={filteredProducts} 
          loading={loading}
          onCartUpdate={loadCartCount}
        />
      </div>

      {/* Floating Cart Button (Mobile) */}
      <Link href="/shop/cart">
        <Button
          className="fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg md:hidden"
          size="icon"
        >
          <ShoppingCart className="h-6 w-6" />
          {cartCount > 0 && (
            <span className="absolute -top-2 -right-2 bg-red-600 text-white text-xs font-bold rounded-full h-6 w-6 flex items-center justify-center">
              {cartCount}
            </span>
          )}
        </Button>
      </Link>
    </div>
  )
}
