'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Settings, Save, Key, Bell, Shield, Database } from 'lucide-react'
import { toast } from 'sonner'

export function SettingsTab() {
  const [settings, setSettings] = useState({
    // API Keys
    openai_key: '',
    paypal_client_id: '',
    paypal_secret: '',
    mercadopago_token: '',
    
    // Notificaciones
    email_notifications: true,
    whatsapp_notifications: false,
    order_notifications: true,
    
    // Seguridad
    require_2fa: false,
    session_timeout: 30,
    
    // Base de datos
    auto_backup: true,
    backup_frequency: 'daily'
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
        <h2 className="text-3xl font-bold text-gray-900">Configuración</h2>
        <p className="text-gray-600 mt-1">Ajustes generales del sistema</p>
      </div>

      <Tabs defaultValue="api" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="api">
            <Key className="w-4 h-4 mr-2" />
            API Keys
          </TabsTrigger>
          <TabsTrigger value="notifications">
            <Bell className="w-4 h-4 mr-2" />
            Notificaciones
          </TabsTrigger>
          <TabsTrigger value="security">
            <Shield className="w-4 h-4 mr-2" />
            Seguridad
          </TabsTrigger>
          <TabsTrigger value="database">
            <Database className="w-4 h-4 mr-2" />
            Base de Datos
          </TabsTrigger>
        </TabsList>

        {/* API Keys */}
        <TabsContent value="api" className="space-y-6 mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Claves de API</CardTitle>
              <CardDescription>
                Configura las claves de servicios externos
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="openai">OpenAI API Key</Label>
                <Input
                  id="openai"
                  type="password"
                  value={settings.openai_key}
                  onChange={(e) => setSettings({ ...settings, openai_key: e.target.value })}
                  placeholder="sk-..."
                />
                <p className="text-xs text-gray-500">
                  Necesaria para las funciones de IA
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="paypal-client">PayPal Client ID</Label>
                <Input
                  id="paypal-client"
                  type="password"
                  value={settings.paypal_client_id}
                  onChange={(e) => setSettings({ ...settings, paypal_client_id: e.target.value })}
                  placeholder="AY..."
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="paypal-secret">PayPal Secret</Label>
                <Input
                  id="paypal-secret"
                  type="password"
                  value={settings.paypal_secret}
                  onChange={(e) => setSettings({ ...settings, paypal_secret: e.target.value })}
                  placeholder="EL..."
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="mercadopago">MercadoPago Access Token</Label>
                <Input
                  id="mercadopago"
                  type="password"
                  value={settings.mercadopago_token}
                  onChange={(e) => setSettings({ ...settings, mercadopago_token: e.target.value })}
                  placeholder="APP_USR-..."
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Notificaciones */}
        <TabsContent value="notifications" className="space-y-6 mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Preferencias de Notificaciones</CardTitle>
              <CardDescription>
                Configura cómo quieres recibir notificaciones
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label htmlFor="email-notif">Notificaciones por Email</Label>
                  <p className="text-sm text-gray-500">
                    Recibe alertas importantes por correo
                  </p>
                </div>
                <Switch
                  id="email-notif"
                  checked={settings.email_notifications}
                  onCheckedChange={(checked) =>
                    setSettings({ ...settings, email_notifications: checked })
                  }
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label htmlFor="whatsapp-notif">Notificaciones por WhatsApp</Label>
                  <p className="text-sm text-gray-500">
                    Recibe alertas en tu WhatsApp
                  </p>
                </div>
                <Switch
                  id="whatsapp-notif"
                  checked={settings.whatsapp_notifications}
                  onCheckedChange={(checked) =>
                    setSettings({ ...settings, whatsapp_notifications: checked })
                  }
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label htmlFor="order-notif">Notificaciones de Pedidos</Label>
                  <p className="text-sm text-gray-500">
                    Alerta cuando hay nuevos pedidos
                  </p>
                </div>
                <Switch
                  id="order-notif"
                  checked={settings.order_notifications}
                  onCheckedChange={(checked) =>
                    setSettings({ ...settings, order_notifications: checked })
                  }
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Seguridad */}
        <TabsContent value="security" className="space-y-6 mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Configuración de Seguridad</CardTitle>
              <CardDescription>
                Protege tu cuenta y datos
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label htmlFor="2fa">Autenticación de Dos Factores</Label>
                  <p className="text-sm text-gray-500">
                    Agrega una capa extra de seguridad
                  </p>
                </div>
                <Switch
                  id="2fa"
                  checked={settings.require_2fa}
                  onCheckedChange={(checked) =>
                    setSettings({ ...settings, require_2fa: checked })
                  }
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="timeout">Tiempo de Sesión (minutos)</Label>
                <Input
                  id="timeout"
                  type="number"
                  value={settings.session_timeout}
                  onChange={(e) =>
                    setSettings({ ...settings, session_timeout: parseInt(e.target.value) })
                  }
                  min="5"
                  max="120"
                />
                <p className="text-xs text-gray-500">
                  Tiempo antes de cerrar sesión automáticamente
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Base de Datos */}
        <TabsContent value="database" className="space-y-6 mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Gestión de Base de Datos</CardTitle>
              <CardDescription>
                Configuración de respaldos y mantenimiento
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label htmlFor="auto-backup">Respaldo Automático</Label>
                  <p className="text-sm text-gray-500">
                    Crea respaldos automáticos de la base de datos
                  </p>
                </div>
                <Switch
                  id="auto-backup"
                  checked={settings.auto_backup}
                  onCheckedChange={(checked) =>
                    setSettings({ ...settings, auto_backup: checked })
                  }
                />
              </div>

              <div className="space-y-4">
                <Button variant="outline" className="w-full">
                  <Database className="w-4 h-4 mr-2" />
                  Crear Respaldo Manual
                </Button>
                <Button variant="outline" className="w-full">
                  <Database className="w-4 h-4 mr-2" />
                  Restaurar desde Respaldo
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      <Button onClick={handleSave} className="w-full">
        <Save className="w-4 h-4 mr-2" />
        Guardar Configuración
      </Button>
    </div>
  )
}
