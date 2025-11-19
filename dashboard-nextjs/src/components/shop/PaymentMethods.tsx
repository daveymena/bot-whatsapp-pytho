'use client'

import { useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { CreditCard, Share2 } from 'lucide-react'
import { toast } from 'sonner'

interface PaymentMethodsProps {
  product: any
  quantity: number
}

export function PaymentMethods({ product, quantity }: PaymentMethodsProps) {
  const [showCODForm, setShowCODForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    address: '',
    notes: ''
  })

  const total = product.price * quantity

  const handleMercadoPago = async () => {
    try {
      toast.loading('Generando link de pago...')
      
      const response = await fetch('http://localhost:5000/payment/create-mercadopago', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          products: [{
            id: product.id,
            name: product.name,
            price: product.price,
            quantity: quantity
          }],
          total: total
        })
      })

      if (response.ok) {
        const data = await response.json()
        toast.success('Link generado!')
        window.open(data.init_point, '_blank')
      } else {
        toast.error('Error al generar link')
      }
    } catch (error) {
      toast.error('Error de conexión')
    }
  }

  const handlePayPal = async () => {
    try {
      toast.loading('Generando link de PayPal...')
      
      const response = await fetch('http://localhost:5000/payment/create-paypal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          products: [{
            id: product.id,
            name: product.name,
            price: product.price,
            quantity: quantity
          }],
          total: total
        })
      })

      if (response.ok) {
        const data = await response.json()
        toast.success('Link generado!')
        window.open(data.approval_url, '_blank')
      } else {
        toast.error('Error al generar link')
      }
    } catch (error) {
      toast.error('Error de conexión')
    }
  }

  const handleCODSubmit = async () => {
    if (!formData.name || !formData.phone || !formData.address) {
      toast.error('Completa todos los campos requeridos')
      return
    }

    try {
      toast.loading('Procesando pedido...')
      
      const response = await fetch('http://localhost:5000/shop/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          products: [{
            id: product.id,
            name: product.name,
            price: product.price,
            quantity: quantity
          }],
          total: total,
          payment_method: 'contraentrega'
        })
      })

      if (response.ok) {
        toast.success('¡Pedido confirmado! Te contactaremos pronto')
        setShowCODForm(false)
        setFormData({ name: '', phone: '', email: '', address: '', notes: '' })
      } else {
        toast.error('Error al procesar pedido')
      }
    } catch (error) {
      toast.error('Error de conexión')
    }
  }

  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-start gap-2 mb-4">
          <CreditCard className="w-5 h-5 text-blue-500 mt-1" />
          <h3 className="font-semibold text-gray-900">Métodos de Pago</h3>
        </div>

        <div className="space-y-3">
          {/* Mercado Pago */}
          <Button
            onClick={handleMercadoPago}
            className="w-full h-12 bg-cyan-500 hover:bg-cyan-600 text-white font-semibold"
          >
            💳 Pagar con MercadoPago
          </Button>

          {/* PayPal */}
          <Button
            onClick={handlePayPal}
            className="w-full h-12 bg-blue-600 hover:bg-blue-700 text-white font-semibold"
          >
            🔵 Pagar con PayPal
          </Button>

          {/* Pago Contraentrega */}
          <Button
            onClick={() => setShowCODForm(true)}
            className="w-full h-12 bg-green-600 hover:bg-green-700 text-white font-semibold"
          >
            💵 Comprar por WhatsApp
          </Button>

          {/* Compartir Producto */}
          <Button
            variant="outline"
            className="w-full h-12 font-semibold"
            onClick={() => {
              navigator.clipboard.writeText(window.location.href)
              toast.success('Link copiado al portapapeles')
            }}
          >
            <Share2 className="w-4 h-4 mr-2" />
            Compartir producto
          </Button>
        </div>

        {/* Dialog para Contra Entrega */}
        <Dialog open={showCODForm} onOpenChange={setShowCODForm}>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>Comprar por WhatsApp</DialogTitle>
            </DialogHeader>
            
            <div className="space-y-4">
              <div>
                <Label htmlFor="name">Nombre completo *</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Tu nombre"
                />
              </div>

              <div>
                <Label htmlFor="phone">Teléfono *</Label>
                <Input
                  id="phone"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  placeholder="+57 300 123 4567"
                />
              </div>

              <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  placeholder="tu@email.com"
                />
              </div>

              <div>
                <Label htmlFor="address">Dirección de entrega *</Label>
                <Textarea
                  id="address"
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  placeholder="Calle, número, ciudad..."
                  rows={3}
                />
              </div>

              <div>
                <Label htmlFor="notes">Notas adicionales</Label>
                <Textarea
                  id="notes"
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  placeholder="Instrucciones especiales..."
                  rows={2}
                />
              </div>

              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm font-medium text-gray-700 mb-1">Resumen del pedido:</p>
                <p className="text-sm text-gray-600">{product.name} x {quantity}</p>
                <p className="text-lg font-bold text-gray-900 mt-2">
                  Total: $ {total.toLocaleString()}
                </p>
              </div>

              <Button
                onClick={handleCODSubmit}
                className="w-full bg-green-600 hover:bg-green-700"
              >
                Confirmar Pedido
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </CardContent>
    </Card>
  )
}
