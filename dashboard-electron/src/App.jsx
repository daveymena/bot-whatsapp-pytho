import { useState, useEffect } from 'react';
import { 
  MessageSquare, Package, Settings, BarChart3, 
  Users, Menu, X, Bell, Bot, ShoppingCart, Brain 
} from 'lucide-react';
import axios from 'axios';
import TitleBar from './components/TitleBar';
import Sidebar from './components/Sidebar';
import Overview from './components/Overview';
import Conversations from './components/Conversations';
import Agents from './components/Agents';

const API_URL = 'http://localhost:3000';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState({
    active_conversations: 0,
    orders_today: 0,
    sales_today: 0,
    conversion_rate: 0
  });

  const menuItems = [
    { id: 'overview', label: 'Resumen', icon: BarChart3 },
    { id: 'whatsapp', label: 'WhatsApp', icon: MessageSquare },
    { id: 'conversations', label: 'Conversaciones', icon: MessageSquare },
    { id: 'products', label: 'Productos', icon: Package },
    { id: 'orders', label: 'Pedidos', icon: ShoppingCart },
    { id: 'agents', label: 'Agentes IA', icon: Brain },
    { id: 'customers', label: 'Clientes', icon: Users },
    { id: 'settings', label: 'Configuración', icon: Settings },
  ];

  useEffect(() => {
    loadStats();
    const interval = setInterval(loadStats, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/admin/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-slate-50 via-green-50/20 to-emerald-50/30">
      {/* Custom Title Bar */}
      <TitleBar />

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <Sidebar 
          isOpen={sidebarOpen}
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          menuItems={menuItems}
        />

        {/* Main Content */}
        <main className={`flex-1 overflow-y-auto transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-0'}`}>
          <div className="p-6">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setSidebarOpen(!sidebarOpen)}
                  className="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-white/50"
                >
                  {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
                </button>
                <div>
                  <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
                  <p className="text-gray-600">Bienvenido al panel de control</p>
                </div>
              </div>
              <button className="p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-white/50">
                <Bell size={20} />
              </button>
            </div>

            {/* Content */}
            {activeTab === 'overview' && <Overview stats={stats} />}
            {activeTab === 'conversations' && <Conversations />}
            {activeTab === 'agents' && <Agents />}
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
