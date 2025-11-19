'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Bot, Package, CreditCard, Calendar, ShoppingBag, Brain, Zap } from 'lucide-react'
import { Badge } from '@/components/ui/badge'

export function AgentsTab() {
  const agents = [
    {
      id: 'professional_sales',
      name: 'Agente de Ventas Profesional',
      description: 'Especialista en ventas con técnicas AIDA y SPIN',
      icon: Bot,
      color: 'blue',
      capabilities: ['AIDA', 'SPIN', 'Manejo de objeciones', 'Cierre', 'Análisis de sentimiento']
    },
    {
      id: 'products',
      name: 'Agente de Productos',
      description: 'Experto en catálogo y productos',
      icon: Package,
      color: 'green',
      capabilities: ['Búsqueda inteligente', 'Comparativas', 'Recomendaciones', 'Stock']
    },
    {
      id: 'dropshipping',
      name: 'Agente de Dropshipping',
      description: 'Especialista en productos Dropi',
      icon: ShoppingBag,
      color: 'purple',
      capabilities: ['Integración Dropi', 'Cálculo de márgenes', 'Sincronización']
    },
    {
      id: 'reservations',
      name: 'Agente de Reservas',
      description: 'Experto en agendamiento de servicios',
      icon: Calendar,
      color: 'orange',
      capabilities: ['Citas', 'Recordatorios', 'Confirmaciones', 'Cancelaciones']
    },
    {
      id: 'payment',
      name: 'Agente de Pagos',
      description: 'Especialista en métodos de pago',
      icon: CreditCard,
      color: 'pink',
      capabilities: ['PayPal', 'MercadoPago', 'Verificación', 'Recibos']
    },
    {
      id: 'multi_domain',
      name: 'Agente Multi-Dominio',
      description: 'Coordinador de múltiples agentes',
      icon: Brain,
      color: 'indigo',
      capabilities: ['Routing', 'Coordinación', 'Escalamiento', 'Contexto']
    },
    {
      id: 'hybrid',
      name: 'Sistema Híbrido',
      description: 'Combina respuestas locales e IA',
      icon: Zap,
      color: 'yellow',
      capabilities: ['Respuestas rápidas', 'IA avanzada', 'Optimización', 'Caché']
    }
  ]

  const colorClasses: Record<string, string> = {
    blue: 'bg-blue-100 text-blue-600 border-blue-200',
    green: 'bg-green-100 text-green-600 border-green-200',
    purple: 'bg-purple-100 text-purple-600 border-purple-200',
    orange: 'bg-orange-100 text-orange-600 border-orange-200',
    pink: 'bg-pink-100 text-pink-600 border-pink-200',
    indigo: 'bg-indigo-100 text-indigo-600 border-indigo-200',
    yellow: 'bg-yellow-100 text-yellow-600 border-yellow-200'
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Agentes Inteligentes</h2>
        <p className="text-gray-600 mt-1">Sistema de agentes especializados con IA</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent) => {
          const Icon = agent.icon
          return (
            <Card key={agent.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className={`w-12 h-12 rounded-lg flex items-center justify-center mb-3 border ${colorClasses[agent.color]}`}>
                  <Icon className="w-6 h-6" />
                </div>
                <CardTitle className="text-lg">{agent.name}</CardTitle>
                <CardDescription>{agent.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {agent.capabilities.map((cap, index) => (
                    <Badge key={index} variant="secondary" className="text-xs">
                      {cap}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Info adicional */}
      <Card className="bg-gradient-to-r from-green-50 to-emerald-50 border-green-200">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-green-600" />
            Sistema de Agentes Inteligentes
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 mb-4">
            El sistema utiliza múltiples agentes especializados que trabajan en conjunto para
            proporcionar la mejor experiencia al cliente. Cada agente tiene capacidades únicas
            y se activa según el contexto de la conversación.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="bg-white p-3 rounded-lg">
              <p className="font-semibold text-gray-900 mb-1">🎯 Detección de Intención</p>
              <p className="text-gray-600">Identifica automáticamente qué necesita el cliente</p>
            </div>
            <div className="bg-white p-3 rounded-lg">
              <p className="font-semibold text-gray-900 mb-1">🔄 Routing Inteligente</p>
              <p className="text-gray-600">Dirige al agente más apropiado</p>
            </div>
            <div className="bg-white p-3 rounded-lg">
              <p className="font-semibold text-gray-900 mb-1">📊 Análisis Continuo</p>
              <p className="text-gray-600">Mejora con cada interacción</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
