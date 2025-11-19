const { default: makeWASocket, DisconnectReason, useMultiFileAuthState, fetchLatestBaileysVersion } = require('@whiskeysockets/baileys');
const express = require('express');
const cors = require('cors');
const qrcode = require('qrcode-terminal');
const axios = require('axios');
const P = require('pino');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = 3002;
const PYTHON_API = 'http://localhost:5000';

let sock = null;
let qrCodeData = null;
let connectionStatus = 'DISCONNECTED';
let phoneNumber = null;
let lastConnectedAt = null;

// Logger
const logger = P({ level: 'silent' });

// Inicializar WhatsApp
async function connectToWhatsApp() {
    try {
        console.log('🔄 Iniciando conexión a WhatsApp...');
        
        const { state, saveCreds } = await useMultiFileAuthState('./auth_info');
        const { version } = await fetchLatestBaileysVersion();

        sock = makeWASocket({
            version,
            logger,
            printQRInTerminal: false,
            auth: state,
            browser: ['Smart Sales Bot', 'Chrome', '1.0.0'],
            defaultQueryTimeoutMs: undefined,
            keepAliveIntervalMs: 10000,
            connectTimeoutMs: 60000,
            markOnlineOnConnect: true,
        });

        // Guardar credenciales
        sock.ev.on('creds.update', saveCreds);

        // Manejar QR Code
        sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            console.log('📱 QR Code generado');
            qrcode.generate(qr, { small: true });
            qrCodeData = qr;
            connectionStatus = 'QR_PENDING';
        }

        if (connection === 'close') {
            const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log('❌ Conexión cerrada. Reconectar:', shouldReconnect);
            
            connectionStatus = 'DISCONNECTED';
            qrCodeData = null;
            phoneNumber = null;

            if (shouldReconnect) {
                setTimeout(() => connectToWhatsApp(), 3000);
            }
        } else if (connection === 'open') {
            console.log('✅ WhatsApp conectado exitosamente!');
            connectionStatus = 'CONNECTED';
            qrCodeData = null;
            lastConnectedAt = new Date().toISOString();
            
            // Obtener número de teléfono
            try {
                const user = sock.user;
                phoneNumber = user.id.split(':')[0];
                console.log(`📱 Número conectado: ${phoneNumber}`);
            } catch (error) {
                console.error('Error obteniendo número:', error);
            }
        } else if (connection === 'connecting') {
            console.log('🔄 Conectando a WhatsApp...');
            connectionStatus = 'CONNECTING';
        }
        });

        // Manejar mensajes entrantes
        sock.ev.on('messages.upsert', async ({ messages, type }) => {
            if (type !== 'notify') return;

            for (const msg of messages) {
            if (!msg.message || msg.key.fromMe) continue;

            const from = msg.key.remoteJid;
            const messageText = msg.message.conversation || 
                               msg.message.extendedTextMessage?.text || 
                               '';

            if (!messageText) continue;

            console.log(`📨 Mensaje de ${from}: ${messageText}`);

                try {
                    // Enviar a Python API
                    const response = await axios.post(`${PYTHON_API}/webhook/message`, {
                        phone: from,
                        message: messageText
                    }, {
                        timeout: 30000
                    });

                    if (response.data && response.data.reply) {
                        // Simular typing
                        await sock.sendPresenceUpdate('composing', from);
                        await new Promise(resolve => setTimeout(resolve, 1000));
                        await sock.sendPresenceUpdate('paused', from);

                        // Enviar respuesta
                        await sock.sendMessage(from, { text: response.data.reply });
                        console.log(`✅ Respuesta enviada a ${from}`);
                    }
                } catch (error) {
                    console.error('❌ Error procesando mensaje:', error.message);
                }
            }
        });
        
    } catch (error) {
        console.error('❌ Error al inicializar WhatsApp:', error);
        connectionStatus = 'DISCONNECTED';
        throw error;
    }
}

// API Endpoints
app.get('/status', (req, res) => {
    res.json({
        success: true,
        status: connectionStatus,
        qrCode: qrCodeData,
        connection: {
            phoneNumber: phoneNumber,
            lastConnectedAt: lastConnectedAt,
            isActive: connectionStatus === 'CONNECTED'
        }
    });
});

app.post('/send-message', async (req, res) => {
    const { phone, message } = req.body;

    if (!sock || connectionStatus !== 'CONNECTED') {
        return res.status(503).json({
            success: false,
            error: 'WhatsApp no está conectado'
        });
    }

    try {
        const jid = phone.includes('@') ? phone : `${phone}@s.whatsapp.net`;
        await sock.sendMessage(jid, { text: message });
        
        res.json({
            success: true,
            message: 'Mensaje enviado correctamente'
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

app.post('/disconnect', async (req, res) => {
    try {
        if (sock) {
            await sock.logout();
            connectionStatus = 'DISCONNECTED';
            qrCodeData = null;
            phoneNumber = null;
        }
        
        res.json({
            success: true,
            message: 'WhatsApp desconectado'
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

app.post('/reconnect', async (req, res) => {
    try {
        // Si ya hay una conexión activa, no hacer nada
        if (connectionStatus === 'CONNECTED') {
            return res.json({
                success: true,
                message: 'WhatsApp ya está conectado',
                status: connectionStatus
            });
        }
        
        // Si ya está conectando, no iniciar otra conexión
        if (connectionStatus === 'CONNECTING' || connectionStatus === 'QR_PENDING') {
            return res.json({
                success: true,
                message: 'WhatsApp ya está en proceso de conexión',
                status: connectionStatus
            });
        }
        
        // Iniciar nueva conexión
        connectToWhatsApp().catch(err => {
            console.error('Error en connectToWhatsApp:', err);
        });
        
        res.json({
            success: true,
            message: 'Reconectando WhatsApp...',
            status: 'CONNECTING'
        });
    } catch (error) {
        console.error('Error en /reconnect:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

app.post('/cleanup', async (req, res) => {
    try {
        const fs = require('fs');
        const path = require('path');
        
        // Desconectar primero
        if (sock) {
            try {
                await sock.logout();
            } catch (e) {
                console.log('Socket ya desconectado');
            }
            sock = null;
        }
        
        // Limpiar estado
        connectionStatus = 'DISCONNECTED';
        qrCodeData = null;
        phoneNumber = null;
        lastConnectedAt = null;
        
        // Eliminar carpeta de autenticación
        const authPath = path.join(__dirname, 'auth_info');
        let filesDeleted = false;
        
        if (fs.existsSync(authPath)) {
            fs.rmSync(authPath, { recursive: true, force: true });
            filesDeleted = true;
            console.log('✅ Carpeta de autenticación eliminada');
        }
        
        res.json({
            success: true,
            message: 'Sesión limpiada correctamente',
            memoryCleared: true,
            filesDeleted: filesDeleted
        });
    } catch (error) {
        console.error('Error limpiando sesión:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Iniciar servidor
app.listen(PORT, () => {
    console.log('='.repeat(60));
    console.log('🚀 SERVIDOR BAILEYS INICIADO');
    console.log('='.repeat(60));
    console.log(`📡 Puerto: ${PORT}`);
    console.log(`🔗 API: http://localhost:${PORT}`);
    console.log(`🐍 Python API: ${PYTHON_API}`);
    console.log('='.repeat(60));
    
    // Conectar a WhatsApp
    connectToWhatsApp();
});

// Manejo de errores
process.on('uncaughtException', (error) => {
    console.error('❌ Error no capturado:', error);
});

process.on('unhandledRejection', (error) => {
    console.error('❌ Promesa rechazada:', error);
});
