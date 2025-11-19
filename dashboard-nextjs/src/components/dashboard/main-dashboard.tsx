'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/hooks/use-auth'
import { useSessionPersistence } from '@/hooks/useSessionPersistence'
import {
  Bot,
  MessageSquare,
  Package,
  Settings,
  BarChart3,
  Users,
  LogOut,
  Menu,
  Bell,
  ChevronDown,
  Loader2,
  Store,
  Brain,
  Zap,
  Shield,
  ShoppingCart
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { toast } from 'sonner'
import { Toaster } from 'sonner'
import { ProductsTab } from '@/components/products/ProductsTab'
import { WhatsAppConnection } from '@/components/dashboard/WhatsAppConnection'
import { AgentsTab } from '@/components/agents/AgentsTab'
import { StoreTab } from '@/components/store/StoreTab'
import { PersonalityTab } from '@/components/personality/PersonalityTab'
import { PromptsTab } from '@/components/prompts/PromptsTab'
import { TrainingTab } from '@/components/training/TrainingTab'
import { ConversationsTab } from '@/components/conversations/ConversationsTab'
import { SettingsTab } from '@/components/settings/SettingsTab'
import { OrdersTab } from '@/components/orders/OrdersTab'

export function MainDashboard() {
  const { user, subscription, logout } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [activeTab, setActiveTab] = useState('overview')
  const [isMobile, setIsMobile] = useState(false)

  // 🔒 Mantener sesión activa automáticamente
  useSessionPersistence()

  // Leer el tab de la URL
  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const tab = params.get('tab')
    if (tab) {
      setActiveTab(tab)
    }
  }, [])

  // Detectar si es móvil
  useEffect(() => {
    const checkMobile = () => {
      const mobile = window.innerWidth < 768
      setIsMobile(mobile)
      if (mobile) {
        setSidebarOpen(false)
        setSidebarCollapsed(false)
      }
    }
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  const menuItems = [
    { id: 'overview', label: 'Resumen', icon: BarChart3 },
    { id: 'whatsapp', label: 'WhatsApp', icon: MessageSquare },
    { id: 'conversations', label: 'Conversaciones', icon: MessageSquare },
    { id: 'products', label: 'Productos', icon: Package },
    { id: 'orders', label: 'Pedidos', icon: ShoppingCart },
    { id: 'agents', label: 'Agentes IA', icon: Brain },
    { id: 'store', label: 'Mi Tienda', icon: Store },
    { id: 'personality', label: 'Personalidad Bot', icon: Bot },
    { id: 'prompts', label: 'IA & Prompts', icon: Brain },
    { id: 'training', label: 'Entrenamiento Bot', icon: Zap },
    { id: 'customers', label: 'Clientes', icon: Users },
    { id: 'settings', label: 'Configuración', icon: Settings },
  ]

  return (
    <>
      <Toaster position="top-right" richColors />
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-green-50/20 to-emerald-50/30">
      {/* Top Navigation */}
      <nav className="bg-white/95 backdrop-blur-sm border-b border-gray-200 fixed w-full z-30 top-0 shadow-sm">
        <div className="px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Left side */}
            <div className="flex items-center gap-2 sm:gap-3">
              <button
                onClick={() => {
                  if (isMobile) {
                    setSidebarOpen(!sidebarOpen)
                  } else {
                    setSidebarCollapsed(!sidebarCollapsed)
                  }
                }}
                className="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none transition-all duration-200"
                aria-label="Toggle menu"
              >
                <Menu className="h-5 w-5 sm:h-6 sm:w-6" />
              </button>
              
              {/* Logo */}
              <div className="flex items-center gap-2">
                <div className="relative flex-shrink-0">
                  <div className="w-9 h-9 sm:w-10 sm:h-10 bg-gradient-to-br from-[#25d366] to-[#128c7e] rounded-xl flex items-center justify-center shadow-lg shadow-[#25d366]/20">
                    <span className="text-white font-bold text-sm sm:text-base tracking-tight">
                      VB
                    </span>
                  </div>
                  <div className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 sm:w-3 sm:h-3 bg-[#25d366] rounded-full border-2 border-white animate-pulse"></div>
                </div>
              </div>
            </div>

            {/* Right side */}
            <div className="flex items-center gap-1 sm:gap-2 md:gap-3">
              {/* Subscription Badge */}
              {subscription && (
                <Badge
                  variant={subscription.hasAccess ? "default" : "destructive"}
                  className="hidden lg:flex text-xs px-2 py-0.5"
                >
                  {subscription.type}
                  {subscription.daysLeft && ` ${subscription.daysLeft}d`}
                </Badge>
              )}

              {/* Notifications */}
              <button
                className="p-1.5 sm:p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
                aria-label="Notificaciones"
              >
                <Bell className="h-4 w-4 sm:h-5 sm:w-5" />
              </button>

              {/* User Menu */}
              <div className="flex items-center gap-1 sm:gap-2">
                <Avatar className="h-8 w-8 sm:h-9 sm:w-9">
                  <AvatarFallback className="bg-green-600 text-white text-sm">
                    {user?.name?.charAt(0) || user?.email?.charAt(0) || 'U'}
                  </AvatarFallback>
                </Avatar>
                <div className="hidden lg:block max-w-[120px]">
                  <p className="text-xs font-medium text-gray-700 truncate leading-tight">
                    {user?.name || 'Usuario'}
                  </p>
                  <p className="text-[10px] text-gray-500 truncate leading-tight">
                    {user?.email}
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => logout()}
                  className="h-8 w-8 sm:h-9 sm:w-9 p-0"
                  aria-label="Cerrar sesión"
                >
                  <LogOut className="h-3.5 w-3.5 sm:h-4 sm:w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Overlay para móvil */}
      {isMobile && sidebarOpen && (
        <div
          className="fixed inset-0 bg-gray-900/40 backdrop-blur-sm z-20 top-16 transition-opacity duration-300"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed left-0 top-16 h-[calc(100vh-4rem)] bg-gradient-to-b from-[#075e54] to-[#128c7e] border-r border-[#128c7e]/30 transition-all duration-300 z-30 shadow-lg ${
          isMobile
            ? sidebarOpen
              ? 'translate-x-0 w-64'
              : '-translate-x-full w-64'
            : sidebarCollapsed
            ? 'w-20'
            : 'w-64'
        }`}
      >
        <nav className="p-3 space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon
            const isActive = activeTab === item.id
            return (
              <button
                key={item.id}
                onClick={() => {
                  setActiveTab(item.id)
                  // Actualizar la URL sin recargar la página
                  window.history.pushState({}, '', `/dashboard?tab=${item.id}`)
                  if (isMobile) setSidebarOpen(false)
                }}
                className={`group w-full flex items-center gap-3 px-4 py-3.5 rounded-xl transition-all duration-200 ${
                  isActive
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border-l-4 border-white'
                    : 'text-white/70 hover:bg-white/10 hover:text-white'
                } ${sidebarCollapsed && !isMobile ? 'justify-center' : ''}`}
                title={sidebarCollapsed && !isMobile ? item.label : ''}
              >
                <Icon
                  className={`h-5 w-5 flex-shrink-0 transition-all duration-200 ${
                    isActive
                      ? 'text-white'
                      : 'text-white/70 group-hover:text-white group-hover:scale-110'
                  }`}
                />
                {(!sidebarCollapsed || isMobile) && (
                  <span className="font-medium text-sm">{item.label}</span>
                )}
                {isActive && (!sidebarCollapsed || isMobile) && (
                  <div className="ml-auto">
                    <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                  </div>
                )}
              </button>
            )
          })}
        </nav>

        {/* Decorative gradient at bottom */}
        <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-[#075e54] via-transparent to-transparent pointer-events-none"></div>
      </aside>

      {/* Main Content */}
      <main
        className={`pt-16 transition-all duration-300 min-h-screen ${
          isMobile
            ? 'ml-0'
            : sidebarCollapsed
            ? 'ml-20'
            : 'ml-64'
        }`}
      >
        <div className="p-4 sm:p-6 lg:p-8">
          <div className="max-w-7xl mx-auto">
            {activeTab === 'overview' && <OverviewTab />}
            {activeTab === 'whatsapp' && <WhatsAppConnection />}
            {activeTab === 'conversations' && <ConversationsTab />}
            {activeTab === 'products' && <ProductsTab />}
            {activeTab === 'orders' && <OrdersTab />}
            {activeTab === 'agents' && <AgentsTab />}
            {activeTab === 'store' && <StoreTab />}
            {activeTab === 'personality' && <PersonalityTab />}
            {activeTab === 'prompts' && <PromptsTab />}
            {activeTab === 'training' && <TrainingTab />}
            {activeTab === 'customers' && <CustomersTab />}
            {activeTab === 'settings' && <SettingsTab />}
          </div>
        </div>
      </main>
    </div>
    </>
  )
}

// Tabs Components
function OverviewTab() {
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
    const interval = setInterval(fetchStats, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:5000/admin/stats')
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-green-600" />
      </div>
    )
  }

  const statCards = [
    {
      label: 'Conversaciones Activas',
      value: stats?.active_conversations || 0,
      icon: MessageSquare,
      color: 'blue'
    },
    {
      label: 'Pedidos Hoy',
      value: stats?.orders_today || 0,
      icon: Package,
      color: 'green'
    },
    {
      label: 'Ventas Hoy',
      value: `$${(stats?.sales_today || 0).toLocaleString()}`,
      icon: BarChart3,
      color: 'purple'
    },
    {
      label: 'Tasa de Conversión',
      value: `${stats?.conversion_rate || 0}%`,
      icon: Zap,
      color: 'orange'
    }
  ]

  const colorClasses: Record<string, string> = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    purple: 'bg-purple-100 text-purple-600',
    orange: 'bg-orange-100 text-orange-600'
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Resumen</h2>
        <p className="text-gray-600 mt-1">Estadísticas de tu bot de ventas</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <Card key={index} className="hover:shadow-md transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">{stat.label}</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                  </div>
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${colorClasses[stat.color]}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Conversaciones por Hora</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-center justify-center text-gray-400">
              <p>Gráfico de conversaciones</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Intenciones Detectadas</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-center justify-center text-gray-400">
              <p>Gráfico de intenciones</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Actividad Reciente</CardTitle>
          <CardDescription>Últimas interacciones del bot</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <p className="text-gray-500 text-center py-8">Cargando actividad...</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}



function CustomersTab() {
  const [customers, setCustomers] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCustomers()
  }, [])

  const fetchCustomers = async () => {
    try {
      const response = await fetch('http://localhost:5000/admin/customers')
      if (response.ok) {
        const data = await response.json()
        setCustomers(data)
      }
    } catch (error) {
      console.error('Error fetching customers:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-green-600" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Clientes</h2>
        <p className="text-gray-600 mt-1">Base de datos de clientes</p>
      </div>

      {customers.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center">
            <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              No hay clientes registrados
            </h3>
            <p className="text-gray-600">
              Los clientes aparecerán aquí cuando interactúen con el bot
            </p>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Cliente
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Teléfono
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Compras
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Total Gastado
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Última Interacción
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {customers.map((customer) => (
                    <tr key={customer.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                            <Users className="w-5 h-5 text-green-600" />
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">
                              {customer.name || 'Sin nombre'}
                            </p>
                            <p className="text-sm text-gray-500">{customer.email || 'Sin email'}</p>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">{customer.phone}</td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {customer.purchase_count || 0}
                      </td>
                      <td className="px-6 py-4 text-sm font-medium text-green-600">
                        ${(customer.total_purchases || 0).toLocaleString()}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500">
                        {customer.last_interaction
                          ? new Date(customer.last_interaction).toLocaleDateString()
                          : 'Nunca'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}


