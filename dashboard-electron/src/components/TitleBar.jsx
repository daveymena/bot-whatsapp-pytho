import { Minus, Square, X } from 'lucide-react';

export default function TitleBar() {
  const handleMinimize = () => {
    if (window.electron) {
      window.electron.minimizeWindow();
    }
  };

  const handleMaximize = () => {
    if (window.electron) {
      window.electron.maximizeWindow();
    }
  };

  const handleClose = () => {
    if (window.electron) {
      window.electron.closeWindow();
    }
  };

  return (
    <div className="h-8 bg-gradient-to-r from-whatsapp-dark to-whatsapp flex items-center justify-between px-4 select-none" style={{ WebkitAppRegion: 'drag' }}>
      <div className="flex items-center gap-2">
        <div className="w-6 h-6 bg-white/20 rounded-lg flex items-center justify-center">
          <span className="text-white text-xs font-bold">SSB</span>
        </div>
        <span className="text-white text-sm font-medium">Smart Sales Bot</span>
      </div>
      
      <div className="flex items-center gap-1" style={{ WebkitAppRegion: 'no-drag' }}>
        <button
          onClick={handleMinimize}
          className="w-8 h-8 flex items-center justify-center text-white/70 hover:text-white hover:bg-white/10 rounded transition-colors"
        >
          <Minus size={16} />
        </button>
        <button
          onClick={handleMaximize}
          className="w-8 h-8 flex items-center justify-center text-white/70 hover:text-white hover:bg-white/10 rounded transition-colors"
        >
          <Square size={14} />
        </button>
        <button
          onClick={handleClose}
          className="w-8 h-8 flex items-center justify-center text-white/70 hover:text-white hover:bg-red-500 rounded transition-colors"
        >
          <X size={16} />
        </button>
      </div>
    </div>
  );
}
