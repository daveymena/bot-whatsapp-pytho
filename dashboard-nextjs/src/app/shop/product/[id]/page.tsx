'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { ShopHeader } from '@/components/shop/ShopHeader'
import { ProductGallery } from '@/components/shop/ProductGallery'
import { ProductDetails } from '@/components/shop/ProductDetails'
import { PaymentMethods } from '@/components/shop/PaymentMethods'
import { Loader2 } from 'lucide-react'
import { toast } from 'sonner'
import { Toaster } from 'sonner'

export default function ProductPage() {
  const params = useParams()
  const router = useRouter()
  const [product, setProduct] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [quantity, setQuantity] = useState(1)
  const [cartCount, setCartCount] = useState(0)

  useEffect(() => {
    loadProduct()
    loadCartCount()
  }, [params.id])

  const loadProduct = async () => {
    try {
      const response = await fetch(`http://localhost:5000/admin/products`)
      if (response.ok) {
        const products = await response.json()
        const foundProduct = products.find((p: any) => p.id === parseInt(params.id as string))
        if (foundProduct) {
          setProduct(foundProduct)
        } else {
          toast.error('Producto no encontrado')
          router.push('/shop')
        }
      }
    } catch (error) {
      console.error('Error:', error)
      toast.error('Error al cargar el producto')
    } finally {
      setLoading(false)
    }
  }

  const loadCartCount = () => {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]')
    setCartCount(cart.reduce((sum: number, item: any) => sum + item.quantity, 0))
  }

  const addToCart = () => {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]')
    const existingItem = cart.find((item: any) => item.id === product.id)

    if (existingItem) {
      existingItem.quantity += quantity
    } else {
      cart.push({
        id: product.id,
        name: product.name,
        price: product.price,
        image_url: product.image_url,
        quantity: quantity
      })
    }

    localStorage.setItem('cart', JSON.stringify(cart))
    loadCartCount()
    toast.success(`${quantity} producto(s) agregado(s) al carrito`)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <ShopHeader cartCount={cartCount} />
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        </div>
      </div>
    )
  }

  if (!product) {
    return null
  }

  return (
    <>
      <Toaster position="top-right" richColors />
      <div className="min-h-screen bg-gray-50">
        <ShopHeader cartCount={cartCount} />
        
        <div className="container mx-auto px-4 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Galería de Imágenes */}
            <ProductGallery 
              images={product.images || [product.image_url]} 
              productName={product.name}
            />

            {/* Detalles del Producto */}
            <div className="space-y-6">
              <ProductDetails 
                product={product}
                quantity={quantity}
                onQuantityChange={setQuantity}
                onAddToCart={addToCart}
              />

              {/* Métodos de Pago */}
              <PaymentMethods 
                product={product}
                quantity={quantity}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
