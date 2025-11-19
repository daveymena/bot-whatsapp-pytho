'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Store, Save, Image, Globe, Phone, Mail, MapPin, CreditCard, DollarSign } from 'lucide-react'
import { toast } from 'sonner'

export function StoreTab() {
  const [storeData, setStoreData] = useState({
    name: 'Mi Tienda',
    description: 'Descripción de mi tienda',
    phone: '',
    email: '',
    address: '',
    website: '',
    logo: ''
  })

  const [paymentMethods, setPaymentMethods] = useState({
    // Mercado Pago
    mercadopago_enabled: false,
    mercadopago_access_token: '',
    
    // PayPal
    paypal_enabled: false,
    paypal_client_id: '',
    paypal_secret: '',
    paypal_mode: 'sandbox',
    
    // Nequi
    nequi_enabled: false,
    nequi_number: '',
    
    // Daviplata
    daviplata_enabled: false,
    daviplata_number: '',
    
    // Banco
    banco_enabled: false,
    bank_name: '',
    bank_account_type: 'Ahorros',
    bank_account_number: '',
    bank_account_holder: '',
    
    // Contra Entrega
    cod_enabled: false,
    cod_zones: ''
  })

  const handleSave = async () => {
    try {
      // Aquí iría la lógica para guardar en el backend
      toast.success('Configuración guardada correctamente')
    } catch (error) {
      toast.error('Error al guardar la configuración')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Mi Tienda</h2>
        <p className="text-gray-600 mt-1">Configura la información de tu tienda y métodos de pago</p>
      </div>

      <Tabs defaultValue="info" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="info">
            <Store className="w-4 h-4 mr-2" />
            Información
          </TabsTrigger>
          <TabsTrigger value="payments">
            <CreditCard className="w-4 h-4 mr-2" />
            Métodos de Pago
          </TabsTrigger>
        </TabsList>

        {/* Tab de Información */}
        <TabsContent value="info" className="space-y-6 mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Formulario */}
            <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Información General</CardTitle>
              <CardDescription>Datos básicos de tu tienda</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Nombre de la Tienda</Label>
                <Input
                  id="name"
                  value={storeData.name}
                  onChange={(e) => setStoreData({ ...storeData, name: e.target.value })}
                  placeholder="Mi Tienda"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Descripción</Label>
                <Textarea
                  id="description"
                  value={storeData.description}
                  onChange={(e) => setStoreData({ ...storeData, description: e.target.value })}
                  placeholder="Describe tu tienda..."
                  rows={4}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="phone">Teléfono</Label>
                  <div className="relative">
                    <Phone className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                    <Input
                      id="phone"
                      value={storeData.phone}
                      onChange={(e) => setStoreData({ ...storeData, phone: e.target.value })}
                      placeholder="+1234567890"
                      className="pl-10"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                    <Input
                      id="email"
                      type="email"
                      value={storeData.email}
                      onChange={(e) => setStoreData({ ...storeData, email: e.target.value })}
                      placeholder="tienda@ejemplo.com"
                      className="pl-10"
                    />
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="address">Dirección</Label>
                <div className="relative">
                  <MapPin className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="address"
                    value={storeData.address}
                    onChange={(e) => setStoreData({ ...storeData, address: e.target.value })}
                    placeholder="Calle Principal 123"
                    className="pl-10"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="website">Sitio Web</Label>
                <div className="relative">
                  <Globe className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="website"
                    value={storeData.website}
                    onChange={(e) => setStoreData({ ...storeData, website: e.target.value })}
                    placeholder="https://mitienda.com"
                    className="pl-10"
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Logo de la Tienda</CardTitle>
              <CardDescription>Sube el logo de tu tienda</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-4">
                <div className="w-24 h-24 bg-gray-100 rounded-lg flex items-center justify-center">
                  {storeData.logo ? (
                    <img src={storeData.logo} alt="Logo" className="w-full h-full object-cover rounded-lg" />
                  ) : (
                    <Image className="w-8 h-8 text-gray-400" />
                  )}
                </div>
                <div className="flex-1">
                  <Input
                    type="file"
                    accept="image/*"
                    onChange={(e) => {
                      // Aquí iría la lógica para subir la imagen
                      toast.info('Funcionalidad de subida de imágenes próximamente')
                    }}
                  />
                  <p className="text-xs text-gray-500 mt-2">
                    Formatos: JPG, PNG. Tamaño máximo: 2MB
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Button onClick={handleSave} className="w-full">
            <Save className="w-4 h-4 mr-2" />
            Guardar Cambios
          </Button>
        </div>

        {/* Vista previa */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Vista Previa</CardTitle>
              <CardDescription>Así se verá tu tienda</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="text-center">
                  <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-green-600 rounded-full mx-auto mb-3 flex items-center justify-center">
                    <Store className="w-10 h-10 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900">{storeData.name}</h3>
                  <p className="text-sm text-gray-600 mt-1">{storeData.description}</p>
                </div>

                <div className="border-t pt-4 space-y-2 text-sm">
                  {storeData.phone && (
                    <div className="flex items-center gap-2 text-gray-600">
                      <Phone className="w-4 h-4" />
                      <span>{storeData.phone}</span>
                    </div>
                  )}
                  {storeData.email && (
                    <div className="flex items-center gap-2 text-gray-600">
                      <Mail className="w-4 h-4" />
                      <span>{storeData.email}</span>
                    </div>
                  )}
                  {storeData.address && (
                    <div className="flex items-center gap-2 text-gray-600">
                      <MapPin className="w-4 h-4" />
                      <span>{storeData.address}</span>
                    </div>
                  )}
                  {storeData.website && (
                    <div className="flex items-center gap-2 text-gray-600">
                      <Globe className="w-4 h-4" />
                      <span>{storeData.website}</span>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
            <CardContent className="pt-6">
              <div className="text-center">
                <Store className="w-8 h-8 text-green-600 mx-auto mb-2" />
                <p className="text-sm text-gray-700">
                  Esta información se mostrará a tus clientes cuando interactúen con el bot
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Vista previa */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Vista Previa</CardTitle>
              <CardDescription>Así se verá tu tienda</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="text-center">
                  <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-green-600 rounded-full mx-auto mb-3 flex items-center justify-center">
                    <Store className="w-10 h-10 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900">{storeData.name}</h3>
                  <p className="text-sm text-gray-600 mt-1">{storeData.description}</p>
                </div>

                <div className="border-t pt-4 space-y-2 text-sm">
                  {storeData.phone && (
                    <div className="flex items-center gap-2 text-gray-600">
                      <Phone className="w-4 h-4" />
                      <span>{storeData.phone}</span>
                    </div>
                  )}
                  {storeData.email && (
                    <div className="flex items-center gap-2 text-gray-600">
                      <Mail className="w-4 h-4" />
                      <span>{storeData.email}</span>
                    </div>
                  )}
                  {storeData.address && (
                    <div className="flex items-center gap-2 text-gray-600">
                      <MapPin className="w-4 h-4" />
                      <span>{storeData.address}</span>
                    </div>
                  )}
                  {storeData.website && (
                    <div className="flex items-center gap-2 text-gray-600">
                      <Globe className="w-4 h-4" />
                      <span>{storeData.website}</span>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
            <CardContent className="pt-6">
              <div className="text-center">
                <Store className="w-8 h-8 text-green-600 mx-auto mb-2" />
                <p className="text-sm text-gray-700">
                  Esta información se mostrará a tus clientes cuando interactúen con el bot
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <Button onClick={handleSave} className="w-full">
        <Save className="w-4 h-4 mr-2" />
        Guardar Información
      </Button>
    </TabsContent>

    {/* Tab de Métodos de Pago */}
    <TabsContent value="payments" className="space-y-6 mt-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Mercado Pago */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              💳 Mercado Pago
            </CardTitle>
            <CardDescription>
              Acepta tarjetas, PSE y pagos en cuotas
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="mp-token">Access Token</Label>
              <Input
                id="mp-token"
                type="password"
                value={paymentMethods.mercadopago_access_token}
                onChange={(e) => setPaymentMethods({ ...paymentMethods, mercadopago_access_token: e.target.value })}
                placeholder="APP_USR-..."
              />
              <p className="text-xs text-gray-500">
                Obtén tu token en: https://www.mercadopago.com/developers
              </p>
            </div>
          </CardContent>
        </Card>

        {/* PayPal */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              🌎 PayPal
            </CardTitle>
            <CardDescription>
              Pagos internacionales seguros
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="paypal-client">Client ID</Label>
              <Input
                id="paypal-client"
                type="password"
                value={paymentMethods.paypal_client_id}
                onChange={(e) => setPaymentMethods({ ...paymentMethods, paypal_client_id: e.target.value })}
                placeholder="AY..."
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="paypal-secret">Secret</Label>
              <Input
                id="paypal-secret"
                type="password"
                value={paymentMethods.paypal_secret}
                onChange={(e) => setPaymentMethods({ ...paymentMethods, paypal_secret: e.target.value })}
                placeholder="EL..."
              />
            </div>
            <p className="text-xs text-gray-500">
              Obtén tus credenciales en: https://developer.paypal.com
            </p>
          </CardContent>
        </Card>

        {/* Nequi */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              💜 Nequi
            </CardTitle>
            <CardDescription>
              Transferencias instantáneas
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="nequi">Número de Nequi</Label>
              <Input
                id="nequi"
                value={paymentMethods.nequi_number}
                onChange={(e) => setPaymentMethods({ ...paymentMethods, nequi_number: e.target.value })}
                placeholder="3001234567"
              />
            </div>
          </CardContent>
        </Card>

        {/* Daviplata */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              ❤️ Daviplata
            </CardTitle>
            <CardDescription>
              Pagos rápidos y seguros
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="daviplata">Número de Daviplata</Label>
              <Input
                id="daviplata"
                value={paymentMethods.daviplata_number}
                onChange={(e) => setPaymentMethods({ ...paymentMethods, daviplata_number: e.target.value })}
                placeholder="3001234567"
              />
            </div>
          </CardContent>
        </Card>

        {/* Transferencia Bancaria */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              🏦 Transferencia Bancaria
            </CardTitle>
            <CardDescription>
              Recibe pagos por transferencia
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="bank-name">Banco</Label>
                <Input
                  id="bank-name"
                  value={paymentMethods.bank_name}
                  onChange={(e) => setPaymentMethods({ ...paymentMethods, bank_name: e.target.value })}
                  placeholder="Bancolombia"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="account-type">Tipo de Cuenta</Label>
                <Input
                  id="account-type"
                  value={paymentMethods.bank_account_type}
                  onChange={(e) => setPaymentMethods({ ...paymentMethods, bank_account_type: e.target.value })}
                  placeholder="Ahorros"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="account-number">Número de Cuenta</Label>
                <Input
                  id="account-number"
                  value={paymentMethods.bank_account_number}
                  onChange={(e) => setPaymentMethods({ ...paymentMethods, bank_account_number: e.target.value })}
                  placeholder="1234567890"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="account-holder">Titular</Label>
                <Input
                  id="account-holder"
                  value={paymentMethods.bank_account_holder}
                  onChange={(e) => setPaymentMethods({ ...paymentMethods, bank_account_holder: e.target.value })}
                  placeholder="Nombre del titular"
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Contra Entrega */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              💵 Pago Contra Entrega
            </CardTitle>
            <CardDescription>
              El cliente paga al recibir el producto
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="cod-zones">Zonas Disponibles</Label>
              <Textarea
                id="cod-zones"
                value={paymentMethods.cod_zones}
                onChange={(e) => setPaymentMethods({ ...paymentMethods, cod_zones: e.target.value })}
                placeholder="Bogotá, Medellín, Cali..."
                rows={3}
              />
              <p className="text-xs text-gray-500">
                Especifica las ciudades o zonas donde ofreces este servicio
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Button onClick={handleSave} className="w-full">
        <Save className="w-4 h-4 mr-2" />
        Guardar Métodos de Pago
      </Button>

      {/* Info Card */}
      <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
        <CardContent className="pt-6">
          <div className="space-y-3">
            <p className="text-sm font-medium text-gray-900">💡 Consejos</p>
            <ul className="text-xs text-gray-600 space-y-2">
              <li>• Configura al menos 2-3 métodos de pago para dar más opciones</li>
              <li>• Mercado Pago y PayPal generan links automáticos</li>
              <li>• Para Nequi, Daviplata y Banco, el cliente debe enviar comprobante</li>
              <li>• El pago contra entrega aumenta las ventas pero requiere logística</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </TabsContent>
  </Tabs>
    </div>
  )
}
