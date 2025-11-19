'use client'

import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ShoppingCart } from 'lucide-react'
import Link from 'next/link'
import { toast } from 'sonner'

interface ProductCardProps {
  product: any
  onCartUpdate: () => void
}

export function ProductCard({ product, onCartUpdate }: ProductCardProps) {
  const addToCart = () => {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]')
    const existingItem = cart.find((item: any) => item.id === product.id)

    if (existingItem) {
      existingItem.quantity += 1
    } else {
      cart.push({
        id: product.id,
        name: product.name,
        price: product.price,
        image_url: product.image_url,
        quantity: 1
      })
    }

    localStorage.setItem('cart', JSON.stringify(cart))
    onCartUpdate()
    toast.success('Producto agregado al carrito')
  }

  // Convertir precio a diferentes monedas
  const priceUSD = (product.price / 4000).toFixed(2)
  const priceEUR = (product.price / 4500).toFixed(2)

  return (
    <Card className="overflow-hidden hover:shadow-xl transition-shadow duration-300 group">
      <Link href={`/shop/product/${product.id}`}>
        <div className="relative aspect-square overflow-hidden bg-gray-100">
          {product.image_url ? (
            <img
              src={product.image_url}
              alt={product.name}
              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-400">
              <ShoppingCart className="w-16 h-16" />
            </div>
          )}
          {product.stock === 0 && (
            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
              <span className="text-white font-bold text-lg">Agotado</span>
            </div>
          )}
        </div>
      </Link>

      <CardContent className="p-4">
        <Link href={`/shop/product/${product.id}`}>
          <h3 className="font-semibold text-lg mb-2 line-clamp-2 hover:text-blue-600 transition-colors">
            {product.name}
          </h3>
        </Link>

        <p className="text-sm text-gray-600 mb-3 line-clamp-2">
          {product.description}
        </p>

        <div className="space-y-1 mb-4">
          <p className="text-2xl font-bold text-gray-900">
            $ {product.price.toLocaleString()}
          </p>
          <p className="text-xs text-gray-500">
            ≈ US$ {priceUSD} | ≈ {priceEUR} €
          </p>
        </div>

        <div className="flex gap-2">
          <Link href={`/shop/product/${product.id}`} className="flex-1">
            <Button variant="outline" className="w-full">
              Ver más
            </Button>
          </Link>
          <Button
            onClick={addToCart}
            disabled={product.stock === 0}
            className="flex-1"
          >
            <ShoppingCart className="w-4 h-4 mr-2" />
            Agregar
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
