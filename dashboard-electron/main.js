const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    backgroundColor: '#f8fafc',
    icon: path.join(__dirname, 'assets', 'icon.png'),
    titleBarStyle: 'hidden',
    frame: false
  });

  // OPCIÓN 1: Panel Admin (FUNCIONA AHORA - mientras arreglas el dashboard)
  mainWindow.loadURL('https://bot-whatsapp-bot-inteligente.sqaoeo.easypanel.host/admin/dashboard');
  
  // OPCIÓN 2: Dashboard Next.js (cuando esté funcionando, descomenta esta línea)
  // mainWindow.loadURL('https://bot-whatsapp-bot-inteligente.sqaoeo.easypanel.host');
  
  // OPCIÓN 2: Desarrollo local (descomenta para usar)
  // if (process.env.NODE_ENV === 'development') {
  //   mainWindow.loadURL('http://localhost:3001');
  //   mainWindow.webContents.openDevTools();
  // } else {
  //   mainWindow.loadFile(path.join(__dirname, 'dist', 'index.html'));
  // }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// IPC Handlers
ipcMain.handle('minimize-window', () => {
  mainWindow.minimize();
});

ipcMain.handle('maximize-window', () => {
  if (mainWindow.isMaximized()) {
    mainWindow.unmaximize();
  } else {
    mainWindow.maximize();
  }
});

ipcMain.handle('close-window', () => {
  mainWindow.close();
});
