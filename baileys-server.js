const { default: makeWASocket, DisconnectReason, useMultiFileAuthState, fetchLatestBaileysVersion } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');
const express = require('express');
const axios = require('axios');
const pino = require('pino');

const app = express();
app.use(express.json());

let sock;
let qrCodeData = null;
let isConnected = false;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 100;
const PYTHON_API_URL = 'http://localhost:3000';

// Logger
const logger = pino({ level: 'info' });

// Inicializar WhatsApp
async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('./data/whatsapp-sessions');
    const { version } = await fetchLatestBaileysVersion();

    sock = makeWASocket({
        version,
        logger: pino({ level: 'silent' }),
        printQRInTerminal: false,
        auth: state,
        browser: ['Tecnovariedades Bot', 'Chrome', '120.0.0'],
        markOnlineOnConnect: true,
        syncFullHistory: false,
        defaultQueryTimeoutMs: 60000,
        connectTimeoutMs: 60000,
        keepAliveIntervalMs: 10000,
        retryRequestDelayMs: 500,
        maxMsgRetryCount: 3,
        msgRetryCounterMap: {},
        getMessage: async (key) => {
            return { conversation: '' };
        }
    });

    // Manejo de conexión
    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            qrCodeData = qr;
            console.log('📱 Escanea este QR con WhatsApp:');
            qrcode.generate(qr, { small: true });
        }

        if (connection === 'close') {
            isConnected = false;
            const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
            
            console.log('❌ Conexión cerrada:', lastDisconnect?.error);
            
            if (shouldReconnect && reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
                reconnectAttempts++;
                const delay = Math.min(500 * Math.pow(2, reconnectAttempts), 60000);
                console.log(`🔄 Reconectando en ${delay}ms (intento ${reconnectAttempts})...`);
                setTimeout(connectToWhatsApp, delay);
            } else if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
                console.log('❌ Máximo de intentos de reconexión alcanzado');
            }
        } else if (connection === 'open') {
            isConnected = true;
            reconnectAttempts = 0;
            qrCodeData = null;
            console.log('✅ Conectado a WhatsApp');
        }
    });

    // Guardar credenciales
    sock.ev.on('creds.update', saveCreds);

    // Manejo de mensajes entrantes
    sock.ev.on('messages.upsert', async ({ messages, type }) => {
        if (type !== 'notify') return;

        for (const msg of messages) {
            if (!msg.message || msg.key.fromMe) continue;

            const from = msg.key.remoteJid;
            const messageText = extractMessageText(msg);

            if (!messageText) continue;

            console.log(`📨 Mensaje de ${from}: ${messageText}`);

            try {
                // Enviar a Python para procesamiento
                const response = await axios.post(`${PYTHON_API_URL}/webhook/message`, {
                    phone: from,
                    message: messageText,
                    timestamp: Date.now()
                });

                if (response.data.reply) {
                    await sendMessage(from, response.data.reply);
                }
            } catch (error) {
                console.error('❌ Error procesando mensaje:', error.message);
            }
        }
    });
}

// Extraer texto del mensaje
function extractMessageText(msg) {
    const messageContent = msg.message;
    
    if (messageContent.conversation) {
        return messageContent.conversation;
    }
    if (messageContent.extendedTextMessage?.text) {
        return messageContent.extendedTextMessage.text;
    }
    if (messageContent.imageMessage?.caption) {
        return messageContent.imageMessage.caption;
    }
    if (messageContent.videoMessage?.caption) {
        return messageContent.videoMessage.caption;
    }
    
    return null;
}

// Enviar mensaje
async function sendMessage(to, text) {
    if (!isConnected) {
        throw new Error('WhatsApp no conectado');
    }

    try {
        await sock.sendMessage(to, { text });
        console.log(`📤 Mensaje enviado a ${to}`);
    } catch (error) {
        console.error('❌ Error enviando mensaje:', error);
        throw error;
    }
}

// Enviar imagen
async function sendImage(to, imageUrl, caption = '') {
    if (!isConnected) {
        throw new Error('WhatsApp no conectado');
    }

    try {
        await sock.sendMessage(to, {
            image: { url: imageUrl },
            caption
        });
        console.log(`📸 Imagen enviada a ${to}`);
    } catch (error) {
        console.error('❌ Error enviando imagen:', error);
        throw error;
    }
}

// Simular typing
async function simulateTyping(to, duration = 2000) {
    try {
        await sock.sendPresenceUpdate('composing', to);
        await new Promise(resolve => setTimeout(resolve, duration));
        await sock.sendPresenceUpdate('paused', to);
    } catch (error) {
        console.error('❌ Error simulando typing:', error);
    }
}

// API REST
app.get('/status', (req, res) => {
    res.json({
        connected: isConnected,
        qrCode: qrCodeData,
        reconnectAttempts
    });
});

app.post('/send-message', async (req, res) => {
    const { phone, message, simulateTyping: shouldSimulate } = req.body;

    if (!phone || !message) {
        return res.status(400).json({ error: 'Phone and message required' });
    }

    try {
        if (shouldSimulate) {
            await simulateTyping(phone, 2000);
        }
        await sendMessage(phone, message);
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/send-image', async (req, res) => {
    const { phone, imageUrl, caption } = req.body;

    if (!phone || !imageUrl) {
        return res.status(400).json({ error: 'Phone and imageUrl required' });
    }

    try {
        await sendImage(phone, imageUrl, caption);
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/qr', (req, res) => {
    if (qrCodeData) {
        res.json({ qr: qrCodeData });
    } else if (isConnected) {
        res.json({ message: 'Already connected' });
    } else {
        res.json({ message: 'Waiting for QR code' });
    }
});

// Iniciar servidor
const PORT = 3001;
app.listen(PORT, () => {
    console.log(`🚀 Baileys server running on port ${PORT}`);
    connectToWhatsApp();
});

// Heartbeat
setInterval(() => {
    if (isConnected && sock) {
        sock.sendPresenceUpdate('available').catch(() => {});
    }
}, 10000);
