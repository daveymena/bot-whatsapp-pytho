import { Bot, Package, CreditCard, Calendar, ShoppingBag } from 'lucide-react';

export default function Agents() {
  const agents = [
    {
      id: 'sales',
      name: 'Agente de Ventas',
      description: 'Especialista en ventas y cierre de negocios',
      icon: Bot,
      color: 'blue',
      capabilities: ['AIDA', 'SPIN', 'Manejo de objeciones', 'Cierre']
    },
    {
      id: 'products',
      name: 'Agente de Productos',
      description: 'Experto en catálogo y productos',
      icon: Package,
      color: 'green',
      capabilities: ['Búsqueda', 'Comparativas', 'Recomendaciones']
    },
    {
      id: 'dropshipping',
      name: 'Agente de Dropshipping',
      description: 'Especialista en productos Dropi',
      icon: ShoppingBag,
      color: 'purple',
      capabilities: ['Integración Dropi', 'Cálculo de márgenes']
    },
    {
      id: 'reservations',
      name: 'Agente de Reservas',
      description: 'Experto en agendamiento de servicios',
      icon: Calendar,
      color: 'orange',
      capabilities: ['Citas', 'Recordatorios', 'Confirmaciones']
    },
    {
      id: 'payment',
      name: 'Agente de Pagos',
      description: 'Especialista en métodos de pago',
      icon: CreditCard,
      color: 'pink',
      capabilities: ['Múltiples métodos', 'Verificación', 'Recibos']
    }
  ];

  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600 border-blue-200',
    green: 'bg-green-100 text-green-600 border-green-200',
    purple: 'bg-purple-100 text-purple-600 border-purple-200',
    orange: 'bg-orange-100 text-orange-600 border-orange-200',
    pink: 'bg-pink-100 text-pink-600 border-pink-200'
  };

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Agentes Inteligentes</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent) => {
          const Icon = agent.icon;
          return (
            <div key={agent.id} className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 hover:shadow-md transition-shadow">
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center mb-4 ${colorClasses[agent.color]}`}>
                <Icon size={24} />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{agent.name}</h3>
              <p className="text-sm text-gray-600 mb-4">{agent.description}</p>
              <div className="flex flex-wrap gap-2">
                {agent.capabilities.map((cap, index) => (
                  <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                    {cap}
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
