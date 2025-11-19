import { MessageSquare, ShoppingCart, DollarSign, TrendingUp } from 'lucide-react';

export default function Overview({ stats }) {
  const statCards = [
    {
      label: 'Conversaciones Activas',
      value: stats.active_conversations,
      icon: MessageSquare,
      color: 'blue'
    },
    {
      label: 'Pedidos Hoy',
      value: stats.orders_today,
      icon: ShoppingCart,
      color: 'green'
    },
    {
      label: 'Ventas Hoy',
      value: `$${stats.sales_today.toLocaleString()}`,
      icon: DollarSign,
      color: 'purple'
    },
    {
      label: 'Tasa de Conversión',
      value: `${stats.conversion_rate}%`,
      icon: TrendingUp,
      color: 'orange'
    }
  ];

  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    purple: 'bg-purple-100 text-purple-600',
    orange: 'bg-orange-100 text-orange-600'
  };

  return (
    <div>
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">{stat.label}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                </div>
                <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${colorClasses[stat.color]}`}>
                  <Icon size={24} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Conversaciones por Hora</h3>
          <div className="h-64 flex items-center justify-center text-gray-400">
            <p>Gráfico de conversaciones</p>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Intenciones Detectadas</h3>
          <div className="h-64 flex items-center justify-center text-gray-400">
            <p>Gráfico de intenciones</p>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Actividad Reciente</h3>
        <div className="space-y-3">
          <p className="text-gray-500 text-center py-8">Cargando actividad...</p>
        </div>
      </div>
    </div>
  );
}
