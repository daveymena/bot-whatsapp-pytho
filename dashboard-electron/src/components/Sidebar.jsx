export default function Sidebar({ isOpen, activeTab, setActiveTab, menuItems }) {
  return (
    <aside
      className={`fixed left-0 top-8 h-[calc(100vh-2rem)] bg-gradient-to-b from-whatsapp-dark to-whatsapp border-r border-whatsapp/30 transition-all duration-300 z-20 shadow-lg ${
        isOpen ? 'w-64 translate-x-0' : 'w-0 -translate-x-full'
      }`}
    >
      <nav className="p-3 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3.5 rounded-xl transition-all duration-200 ${
                isActive
                  ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border-l-4 border-white'
                  : 'text-white/70 hover:bg-white/10 hover:text-white'
              }`}
            >
              <Icon size={20} />
              <span className="font-medium">{item.label}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}
