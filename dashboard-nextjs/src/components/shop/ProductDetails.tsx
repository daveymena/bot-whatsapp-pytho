'use client'

import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ShoppingCart, Minus, Plus, Package, Shield, Truck } from 'lucide-react'

interface ProductDetailsProps {
  product: any
  quantity: number
  onQuantityChange: (quantity: number) => void
  onAddToCart: () => void
}

export function ProductDetails({ product, quantity, onQuantityChange, onAddToCart }: ProductDetailsProps) {
  const priceUSD = (product.price / 4000).toFixed(2)
  const totalCOP = product.price * quantity

  return (
    <div className="space-y-6">
      {/* Badge de Disponibilidad */}
      {product.stock > 0 ? (
        <Badge className="bg-green-100 text-green-700 hover:bg-green-100">
          ✓ 481 disponible
        </Badge>
      ) : (
        <Badge variant="destructive">Agotado</Badge>
      )}

      {/* Título */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {product.name}
        </h1>
      </div>

      {/* Precio */}
      <div className="bg-gradient-to-r from-pink-50 to-purple-50 rounded-lg p-6">
        <div className="flex items-baseline gap-3">
          <span className="text-4xl font-bold text-pink-600">
            $ {product.price.toLocaleString()}
          </span>
          <Badge className="bg-green-500 text-white">✓ 481 disponible</Badge>
        </div>
        
        {/* Conversión de Moneda */}
        <Card className="mt-4 bg-white/80">
          <CardContent className="p-4">
            <div className="flex items-start gap-2">
              <div className="text-blue-600 mt-1">ⓘ</div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-700 mb-1">Conversión de pago</p>
                <p className="text-sm text-gray-600">
                  Precio de la moneda: <span className="font-semibold">$ {product.price.toLocaleString()}</span>
                </p>
                <p className="text-sm text-gray-600">
                  Al pagar se convertirá a <span className="font-semibold">US$ {priceUSD}</span>
                </p>
                <p className="text-xs text-gray-500 mt-1">Tipo: 1 USD = $4000 COP</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Descripción */}
      <Card>
        <CardContent className="p-4">
          <div className="flex items-start gap-2">
            <div className="text-pink-500 mt-1">📝</div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Descripción del Producto</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                {product.description || 'Sin descripción disponible'}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Información del Producto */}
      <Card>
        <CardContent className="p-4">
          <div className="flex items-start gap-2 mb-4">
            <div className="text-blue-500 mt-1">ℹ️</div>
            <h3 className="font-semibold text-gray-900">Información del Producto</h3>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center gap-2">
              <Package className="w-5 h-5 text-orange-500" />
              <div>
                <p className="text-xs text-gray-500">CATEGORÍA</p>
                <p className="text-sm font-medium">{product.category || 'Producto Físico'}</p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <Package className="w-5 h-5 text-blue-500" />
              <div>
                <p className="text-xs text-gray-500">DISPONIBILIDAD</p>
                <p className="text-sm font-medium">{product.stock} unidades</p>
              </div>
            </div>

            {product.warranty && (
              <div className="flex items-center gap-2">
                <Shield className="w-5 h-5 text-orange-500" />
                <div>
                  <p className="text-xs text-gray-500">PRECIO/UNIDAD</p>
                  <p className="text-sm font-medium">$ {product.price.toLocaleString()}</p>
                </div>
              </div>
            )}

            <div className="flex items-center gap-2">
              <Truck className="w-5 h-5 text-blue-500" />
              <div>
                <p className="text-xs text-gray-500">ENVÍO</p>
                <p className="text-sm font-medium">A todo el país</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Beneficios */}
      <Card className="bg-gradient-to-r from-yellow-50 to-orange-50">
        <CardContent className="p-4">
          <div className="flex items-start gap-2 mb-3">
            <div className="text-yellow-600 mt-1">⚡</div>
            <h3 className="font-semibold text-gray-900">Beneficios de Comprar Aquí</h3>
          </div>
          
          <div className="grid grid-cols-3 gap-3">
            <div className="bg-white rounded-lg p-3 text-center">
              <div className="text-2xl mb-1">🚀</div>
              <p className="text-xs font-medium text-gray-700">Envío Rápido</p>
              <p className="text-xs text-gray-500">24-48 horas</p>
            </div>
            
            <div className="bg-white rounded-lg p-3 text-center">
              <div className="text-2xl mb-1">🔒</div>
              <p className="text-xs font-medium text-gray-700">Compra Segura</p>
              <p className="text-xs text-gray-500">100% protegido</p>
            </div>
            
            <div className="bg-white rounded-lg p-3 text-center">
              <div className="text-2xl mb-1">💳</div>
              <p className="text-xs font-medium text-gray-700">Pago Fácil</p>
              <p className="text-xs text-gray-500">Múltiples métodos</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Selector de Cantidad */}
      <Card>
        <CardContent className="p-4">
          <div className="flex items-start gap-2 mb-3">
            <div className="text-orange-500 mt-1">📦</div>
            <h3 className="font-semibold text-gray-900">Cantidad</h3>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center border-2 border-gray-200 rounded-lg">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onQuantityChange(Math.max(1, quantity - 1))}
                disabled={quantity <= 1}
                className="h-12 w-12"
              >
                <Minus className="h-4 w-4" />
              </Button>
              
              <span className="w-16 text-center text-xl font-bold">
                {quantity}
              </span>
              
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onQuantityChange(Math.min(product.stock, quantity + 1))}
                disabled={quantity >= product.stock}
                className="h-12 w-12"
              >
                <Plus className="h-4 w-4" />
              </Button>
            </div>

            <div className="flex-1">
              <p className="text-sm text-gray-600">Total:</p>
              <p className="text-2xl font-bold text-gray-900">
                $ {totalCOP.toLocaleString()}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Botón Agregar al Carrito */}
      <Button
        onClick={onAddToCart}
        disabled={product.stock === 0}
        className="w-full h-14 text-lg font-semibold bg-orange-500 hover:bg-orange-600"
      >
        <ShoppingCart className="w-5 h-5 mr-2" />
        AGREGAR AL CARRITO
      </Button>
    </div>
  )
}
