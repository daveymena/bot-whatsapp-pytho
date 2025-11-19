'use client'

import { useState, useEffect } from 'react'
import { Loader2, Smartphone, CheckCircle2, XCircle, RefreshCw } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { toast } from 'sonner'
import { QRCodeSVG } from 'qrcode.react'

interface WhatsAppStatus {
  success: boolean
  status: 'CONNECTED' | 'DISCONNECTED' | 'QR_PENDING' | 'CONNECTING'
  qrCode?: string
  connection: {
    phoneNumber?: string
    lastConnectedAt?: string
    isActive: boolean
  }
}

export function WhatsAppTab() {
  const [status, setStatus] = useState<WhatsAppStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [connectionError, setConnectionError] = useState<string | null>(null)

  useEffect(() => {
    fetchStatus()
    // Actualizar cada 3 segundos
    const interval = setInterval(fetchStatus, 3000)
    return () => clearInterval(interval)
  }, [])

  const fetchStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/admin/whatsapp/status', {
        signal: AbortSignal.timeout(5000) // 5 segundos timeout
      })
      if (response.ok) {
        const data = await response.json()
        setStatus(data)
        setConnectionError(null)
      } else {
        // Si hay error, establecer estado desconectado
        setConnectionError('No se pudo conectar con el servidor de Python')
        setStatus({
          success: false,
          status: 'DISCONNECTED',
          connection: {
            phoneNumber: undefined,
            lastConnectedAt: undefined,
            isActive: false
          }
        })
      }
    } catch (error) {
      console.error('Error fetching WhatsApp status:', error)
      // Si hay error de conexión, establecer estado desconectado
      setConnectionError('Error de conexión con el servidor. Verifica que el servidor de Python esté corriendo en el puerto 5000.')
      setStatus({
        success: false,
        status: 'DISCONNECTED',
        connection: {
          phoneNumber: undefined,
          lastConnectedAt: undefined,
          isActive: false
        }
      })
    } finally {
      setLoading(false)
    }
  }

  const handleDisconnect = async () => {
    if (!confirm('¿Estás seguro de desconectar WhatsApp?')) return

    setActionLoading(true)
    try {
      const response = await fetch('http://localhost:5000/admin/whatsapp/disconnect', {
        method: 'POST'
      })
      
      if (response.ok) {
        toast.success('WhatsApp desconectado correctamente')
        fetchStatus()
      } else {
        toast.error('Error al desconectar WhatsApp')
      }
    } catch (error) {
      toast.error('Error al desconectar WhatsApp')
    } finally {
      setActionLoading(false)
    }
  }

  const handleReconnect = async () => {
    setActionLoading(true)
    setConnectionError(null)
    try {
      const response = await fetch('http://localhost:5000/admin/whatsapp/reconnect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          toast.success('Reconectando WhatsApp...')
          // Esperar un poco y actualizar el estado
          setTimeout(() => {
            fetchStatus()
          }, 2000)
        } else {
          toast.error(data.error || 'Error al reconectar WhatsApp')
          setConnectionError(data.error || 'Error al reconectar WhatsApp')
        }
      } else {
        toast.error('Error al reconectar WhatsApp')
        setConnectionError('No se pudo conectar con el servidor')
      }
    } catch (error) {
      console.error('Error reconnecting:', error)
      toast.error('Error de conexión. Verifica que el servidor esté corriendo.')
      setConnectionError('Error de conexión. Verifica que el servidor de Python (puerto 5000) y Baileys (puerto 3002) estén corriendo.')
    } finally {
      setActionLoading(false)
    }
  }

  const handleCleanup = async () => {
    if (!confirm('¿Estás seguro de limpiar la sesión? Esto eliminará todos los datos de autenticación.')) return

    setActionLoading(true)
    setConnectionError(null)
    try {
      // Limpiar directamente en el servidor Baileys
      const response = await fetch('http://localhost:3002/cleanup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          toast.success('Sesión limpiada correctamente')
          // Esperar y reconectar
          setTimeout(async () => {
            await handleReconnect()
          }, 2000)
        } else {
          toast.error(data.error || 'Error al limpiar sesión')
          setConnectionError(data.error || 'Error al limpiar sesión')
        }
      } else {
        toast.error('Error al limpiar sesión')
        setConnectionError('No se pudo conectar con el servidor Baileys')
      }
    } catch (error) {
      console.error('Error cleaning up:', error)
      toast.error('Error de conexión. Verifica que el servidor Baileys esté corriendo.')
      setConnectionError('Error de conexión. Verifica que el servidor Baileys (puerto 3002) esté corriendo.')
    } finally {
      setActionLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-green-600" />
      </div>
    )
  }

  const isConnected = status?.status === 'CONNECTED'
  const hasQR = status?.qrCode && status?.status === 'QR_PENDING'
  const isConnecting = status?.status === 'CONNECTING'

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-gray-900">WhatsApp</h2>
        <p className="text-gray-600 mt-1">Gestiona la conexión de tu bot</p>
      </div>

      {/* Status Card */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              {/* Status Indicator */}
              <div className="relative">
                <div className={`w-16 h-16 rounded-full flex items-center justify-center ${
                  isConnected 
                    ? 'bg-green-100' 
                    : hasQR 
                    ? 'bg-yellow-100' 
                    : 'bg-red-100'
                }`}>
                  {isConnected ? (
                    <CheckCircle2 className="w-8 h-8 text-green-600" />
                  ) : hasQR ? (
                    <Smartphone className="w-8 h-8 text-yellow-600" />
                  ) : (
                    <XCircle className="w-8 h-8 text-red-600" />
                  )}
                </div>
                {isConnected && (
                  <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-4 border-white animate-pulse"></div>
                )}
              </div>

              {/* Status Info */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="text-xl font-semibold text-gray-900">
                    {isConnected 
                      ? 'Conectado' 
                      : isConnecting
                      ? 'Conectando...'
                      : hasQR 
                      ? 'Esperando escaneo' 
                      : 'Desconectado'}
                  </h3>
                  <Badge variant={isConnected ? 'default' : 'secondary'}>
                    {status?.status}
                  </Badge>
                </div>
                <p className="text-sm text-gray-600">
                  {isConnected && status?.connection?.phoneNumber
                    ? `Número: +${status.connection.phoneNumber}`
                    : hasQR
                    ? 'Escanea el código QR con tu teléfono'
                    : 'Sin conexión activa'}
                </p>
                {isConnected && status?.connection?.lastConnectedAt && (
                  <p className="text-xs text-gray-500 mt-1">
                    Última conexión: {new Date(status.connection.lastConnectedAt).toLocaleString('es-ES')}
                  </p>
                )}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-2">
              {isConnected && (
                <Button
                  variant="outline"
                  onClick={handleDisconnect}
                  disabled={actionLoading}
                  className="text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                  {actionLoading ? (
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  ) : null}
                  Desconectar
                </Button>
              )}
              {!isConnected && !hasQR && !isConnecting && (
                <Button
                  onClick={handleReconnect}
                  disabled={actionLoading}
                  className="bg-green-600 hover:bg-green-700"
                >
                  {actionLoading ? (
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  ) : (
                    <RefreshCw className="w-4 h-4 mr-2" />
                  )}
                  Reconectar
                </Button>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* QR Code Section */}
      {hasQR && status?.qrCode && (
        <Card>
          <CardHeader>
            <CardTitle>Escanea el Código QR</CardTitle>
            <CardDescription>
              Abre WhatsApp en tu teléfono y escanea este código para conectar el bot
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col items-center">
              {/* QR Code */}
              <div className="bg-white p-6 rounded-2xl shadow-xl border-4 border-green-500 mb-6">
                <QRCodeSVG
                  value={status.qrCode}
                  size={288}
                  level="H"
                  includeMargin={true}
                  className="w-72 h-72"
                />
              </div>

              {/* Instructions */}
              <div className="max-w-md space-y-3">
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-green-600 font-semibold text-sm">1</span>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">Abre WhatsApp en tu teléfono</p>
                    <p className="text-sm text-gray-600">Asegúrate de tener la última versión instalada</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-green-600 font-semibold text-sm">2</span>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">Ve a Configuración</p>
                    <p className="text-sm text-gray-600">Toca los tres puntos (⋮) y selecciona "Dispositivos vinculados"</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-green-600 font-semibold text-sm">3</span>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">Vincular un dispositivo</p>
                    <p className="text-sm text-gray-600">Toca "Vincular un dispositivo" y escanea este código</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-green-600 font-semibold text-sm">4</span>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">¡Listo!</p>
                    <p className="text-sm text-gray-600">Tu bot estará conectado y listo para responder mensajes</p>
                  </div>
                </div>
              </div>

              {/* Refresh Button */}
              <Button
                variant="outline"
                onClick={fetchStatus}
                className="mt-6"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Actualizar estado
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Connection Info */}
      {isConnected && (
        <Card>
          <CardHeader>
            <CardTitle>Información de Conexión</CardTitle>
            <CardDescription>Detalles de la conexión activa</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center py-3 border-b">
                <span className="text-gray-600 font-medium">Número de teléfono</span>
                <span className="font-semibold text-gray-900">
                  +{status?.connection?.phoneNumber || 'N/A'}
                </span>
              </div>

              <div className="flex justify-between items-center py-3 border-b">
                <span className="text-gray-600 font-medium">Estado</span>
                <Badge className="bg-green-100 text-green-800">
                  Activo
                </Badge>
              </div>

              {status?.connection?.lastConnectedAt && (
                <div className="flex justify-between items-center py-3 border-b">
                  <span className="text-gray-600 font-medium">Última conexión</span>
                  <span className="font-medium text-gray-900">
                    {new Date(status.connection.lastConnectedAt).toLocaleString('es-ES', {
                      dateStyle: 'medium',
                      timeStyle: 'short'
                    })}
                  </span>
                </div>
              )}

              <div className="flex justify-between items-center py-3">
                <span className="text-gray-600 font-medium">Servidor</span>
                <span className="font-medium text-gray-900">Baileys (Puerto 3002)</span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Connecting State */}
      {isConnecting && (
        <Card>
          <CardContent className="p-12 text-center">
            <Loader2 className="w-12 h-12 text-green-600 mx-auto mb-4 animate-spin" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Conectando a WhatsApp...
            </h3>
            <p className="text-gray-600">
              Por favor espera mientras establecemos la conexión
            </p>
          </CardContent>
        </Card>
      )}

      {/* Connection Error Alert */}
      {connectionError && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="p-4">
            <div className="flex items-start gap-3">
              <XCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <h4 className="font-semibold text-red-900 mb-1">Error al conectar WhatsApp</h4>
                <p className="text-sm text-red-700">{connectionError}</p>
                <p className="text-xs text-red-600 mt-2">
                  Si el problema persiste, limpia la sesión y genera un nuevo QR.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Disconnected State */}
      {!isConnected && !hasQR && !isConnecting && (
        <Card>
          <CardContent className="p-12 text-center">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <XCircle className="w-8 h-8 text-red-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              WhatsApp Desconectado
            </h3>
            <p className="text-gray-600 mb-6">
              El bot no está conectado a WhatsApp. Haz clic en "Reconectar" para generar un nuevo código QR.
            </p>
            <div className="flex gap-3 justify-center">
              <Button
                onClick={handleReconnect}
                disabled={actionLoading}
                className="bg-green-600 hover:bg-green-700"
              >
                {actionLoading ? (
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                ) : (
                  <RefreshCw className="w-4 h-4 mr-2" />
                )}
                Reconectar
              </Button>
              <Button
                onClick={handleCleanup}
                disabled={actionLoading}
                variant="outline"
                className="text-red-600 hover:text-red-700 hover:bg-red-50"
              >
                {actionLoading ? (
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                ) : null}
                Limpiar Sesión
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
