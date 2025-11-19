# 🚀 PLAN DE IMPLEMENTACIÓN PASO A PASO

## 📋 GUÍA COMPLETA PARA MIGRAR TODAS LAS FUNCIONALIDADES

Este documento contiene el plan detallado para implementar TODAS las funcionalidades
faltantes del bot original en nuestro sistema actual.

---

## 🎯 FASE 1: AUTENTICACIÓN COMPLETA (Semana 1)

### 1.1 Registro de Usuarios

#### Backend: Crear tabla de códigos de verificación
```python
# database/models.py - AGREGAR

class VerificationCode(Base):
    __tablename__ = "verification_codes"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('admin_users.id'))
    code = Column(String(6))
    type = Column(String)  # email, phone, password_reset
    expires_at = Column(DateTime)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### Backend: Servicio de Email
```python
# services/email_service.py - CREAR NUEVO

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
    
    def generate_code(self, length=6):
        return ''.join(random.choices(string.digits, k=length))
    
    async def send_verification_email(self, email, code):
        subject = "Verifica tu email - Bot WhatsApp"
        body = f"""
        <h2>Verificación de Email</h2>
        <p>Tu código de verificación es:</p>
        <h1 style="color: #4F46E5;">{code}</h1>
        <p>Este código expira en 15 minutos.</p>
        """
        return await self._send_email(email, subject, body)
```

    async def send_password_reset_email(self, email, code):
        subject = "Recupera tu contraseña - Bot WhatsApp"
        body = f"""
        <h2>Recuperación de Contraseña</h2>
        <p>Tu código de recuperación es:</p>
        <h1 style="color: #4F46E5;">{code}</h1>
        <p>Este código expira en 15 minutos.</p>
        """
        return await self._send_email(email, subject, body)
    
    async def _send_email(self, to_email, subject, html_body):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.smtp_user
        msg['To'] = to_email
        
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
```

#### Backend: Rutas de Registro
```python
# admin/auth_routes.py - AGREGAR

@auth_bp.route('/register', methods=['POST'])
async def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone = data.get('phone')
    
    # Validar datos
    if not email or not password or not name:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    # Verificar si el email ya existe
    existing_user = db.query(AdminUser).filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    # Crear usuario
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = AdminUser(
        email=email,
        password=hashed_password.decode('utf-8'),
        name=name,
        phone=phone,
        email_verified=False,
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    
    # Generar código de verificación
    email_service = EmailService()
    code = email_service.generate_code()
    
    verification = VerificationCode(
        user_id=new_user.id,
        code=code,
        type='email',
        expires_at=datetime.utcnow() + timedelta(minutes=15)
    )
    db.add(verification)
    db.commit()
    
    # Enviar email
    await email_service.send_verification_email(email, code)
    
    return jsonify({
        'message': 'Usuario registrado. Verifica tu email.',
        'user_id': new_user.id
    }), 201

@auth_bp.route('/verify-email', methods=['POST'])
async def verify_email():
    data = request.json
    user_id = data.get('user_id')
    code = data.get('code')
    
    # Buscar código
    verification = db.query(VerificationCode).filter_by(
        user_id=user_id,
        code=code,
        type='email',
        used=False
    ).first()
    
    if not verification:
        return jsonify({'error': 'Código inválido'}), 400
    
    if verification.expires_at < datetime.utcnow():
        return jsonify({'error': 'Código expirado'}), 400
    
    # Marcar como verificado
    user = db.query(AdminUser).get(user_id)
    user.email_verified = True
    verification.used = True
    db.commit()
    
    return jsonify({'message': 'Email verificado correctamente'}), 200
```

#### Frontend: Página de Registro
```typescript
// dashboard-nextjs/src/app/register/page.tsx - CREAR NUEVO

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';

export default function RegisterPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (formData.password !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }
    
    setLoading(true);
    
    try {
      const response = await fetch('http://localhost:5000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          phone: formData.phone,
          password: formData.password
        })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        // Redirigir a verificación
        router.push(`/verify-email?user_id=${data.user_id}`);
      } else {
        setError(data.error || 'Error al registrar');
      }
    } catch (err) {
      setError('Error de conexión');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md p-8">
        <h1 className="text-2xl font-bold mb-6">Crear Cuenta</h1>
        
        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded mb-4">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Nombre</label>
            <Input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <Input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Teléfono</label>
            <Input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({...formData, phone: e.target.value})}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Contraseña</label>
            <Input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Confirmar Contraseña</label>
            <Input
              type="password"
              value={formData.confirmPassword}
              onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
              required
            />
          </div>
          
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Registrando...' : 'Crear Cuenta'}
          </Button>
        </form>
        
        <p className="text-center mt-4 text-sm text-gray-600">
          ¿Ya tienes cuenta?{' '}
          <a href="/login" className="text-blue-600 hover:underline">
            Inicia sesión
          </a>
        </p>
      </Card>
    </div>
  );
}
```

---

## 🎯 FASE 2: SISTEMA DE MEMBRESÍAS (Semana 2)

### 2.1 Tablas de Base de Datos

```python
# database/models.py - AGREGAR

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)  # Free, Basic, Pro, Enterprise
    slug = Column(String, unique=True)
    price_monthly = Column(Float)
    price_yearly = Column(Float)
    features = Column(JSON)
    limits = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True)
    admin_user_id = Column(Integer, ForeignKey('admin_users.id'))
    plan_id = Column(Integer, ForeignKey('subscription_plans.id'))
    status = Column(String)  # active, cancelled, expired, trial
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    auto_renew = Column(Boolean, default=True)
    payment_method = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class UsageMetrics(Base):
    __tablename__ = "usage_metrics"
    
    id = Column(Integer, primary_key=True)
    admin_user_id = Column(Integer, ForeignKey('admin_users.id'))
    metric_type = Column(String)  # messages, products, orders
    count = Column(Integer, default=0)
    period = Column(String)  # monthly, daily
    date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 2.2 Servicio de Suscripciones

```python
# services/subscription_service.py - CREAR NUEVO

from datetime import datetime, timedelta
from database.models import Subscription, SubscriptionPlan, UsageMetrics

class SubscriptionService:
    def __init__(self, db):
        self.db = db
    
    def get_user_subscription(self, user_id):
        """Obtener suscripción activa del usuario"""
        return self.db.query(Subscription).filter_by(
            admin_user_id=user_id,
            status='active'
        ).first()
    
    def check_limit(self, user_id, metric_type):
        """Verificar si el usuario ha alcanzado su límite"""
        subscription = self.get_user_subscription(user_id)
        if not subscription:
            return False, "No hay suscripción activa"
        
        plan = self.db.query(SubscriptionPlan).get(subscription.plan_id)
        limits = plan.limits
        
        # Obtener uso actual del mes
        today = datetime.utcnow().date()
        first_day = today.replace(day=1)
        
        usage = self.db.query(UsageMetrics).filter(
            UsageMetrics.admin_user_id == user_id,
            UsageMetrics.metric_type == metric_type,
            UsageMetrics.date >= first_day
        ).first()
        
        current_count = usage.count if usage else 0
        limit = limits.get(metric_type, float('inf'))
        
        if current_count >= limit:
            return False, f"Límite de {metric_type} alcanzado"
        
        return True, current_count
    
    def increment_usage(self, user_id, metric_type):
        """Incrementar contador de uso"""
        today = datetime.utcnow().date()
        
        usage = self.db.query(UsageMetrics).filter_by(
            admin_user_id=user_id,
            metric_type=metric_type,
            date=today
        ).first()
        
        if usage:
            usage.count += 1
        else:
            usage = UsageMetrics(
                admin_user_id=user_id,
                metric_type=metric_type,
                count=1,
                period='monthly',
                date=today
            )
            self.db.add(usage)
        
        self.db.commit()
```

---

## 🎯 FASE 3: PROCESAMIENTO MULTIMEDIA (Semana 3)

### 3.1 Procesamiento de Audio

```python
# whatsapp/audio_handler.py - CREAR NUEVO

import openai
from gtts import gTTS
import os
from pathlib import Path

class AudioHandler:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_key
        self.temp_dir = Path('temp-media/audio')
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    async def transcribe_audio(self, audio_path):
        """Transcribir audio a texto usando Whisper"""
        try:
            with open(audio_path, 'rb') as audio_file:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="es"
                )
            return transcript.text
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
    
    async def text_to_speech(self, text, language='es'):
        """Convertir texto a audio"""
        try:
            output_path = self.temp_dir / f"tts_{datetime.now().timestamp()}.mp3"
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(str(output_path))
            return str(output_path)
        except Exception as e:
            print(f"Error generating speech: {e}")
            return None
    
    async def process_audio_message(self, phone, audio_data):
        """Procesar mensaje de audio completo"""
        # Guardar audio temporalmente
        audio_path = self.temp_dir / f"audio_{phone}_{datetime.now().timestamp()}.ogg"
        with open(audio_path, 'wb') as f:
            f.write(audio_data)
        
        # Transcribir
        text = await self.transcribe_audio(audio_path)
        
        # Limpiar archivo temporal
        os.remove(audio_path)
        
        return text
```

### 3.2 Procesamiento Avanzado de Imágenes

```python
# whatsapp/image_processor.py - MEJORAR

import openai
from PIL import Image
import pytesseract
import base64
from io import BytesIO

class ImageProcessor:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_key
    
    async def analyze_image_with_ai(self, image_path):
        """Analizar imagen con GPT-4 Vision"""
        try:
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analiza esta imagen y describe qué ves. Si es un comprobante de pago, extrae: monto, fecha, referencia."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return None
    
    async def extract_text_ocr(self, image_path):
        """Extraer texto de imagen con OCR"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='spa')
            return text
        except Exception as e:
            print(f"Error in OCR: {e}")
            return None
    
    async def detect_payment_proof(self, image_path):
        """Detectar si es comprobante de pago"""
        # Analizar con IA
        analysis = await self.analyze_image_with_ai(image_path)
        
        # Extraer texto con OCR
        ocr_text = await self.extract_text_ocr(image_path)
        
        # Buscar palabras clave
        payment_keywords = ['pago', 'transferencia', 'comprobante', 'monto', 'referencia']
        is_payment = any(keyword in analysis.lower() or keyword in ocr_text.lower() 
                        for keyword in payment_keywords)
        
        return {
            'is_payment_proof': is_payment,
            'analysis': analysis,
            'extracted_text': ocr_text
        }
```

---

## 📝 CHECKLIST DE IMPLEMENTACIÓN

### Semana 1: Autenticación
- [ ] Crear tabla VerificationCode
- [ ] Implementar EmailService
- [ ] Ruta /register
- [ ] Ruta /verify-email
- [ ] Ruta /forgot-password
- [ ] Ruta /reset-password
- [ ] Página de registro
- [ ] Página de verificación
- [ ] Página de recuperación

### Semana 2: Membresías
- [ ] Crear tablas de suscripciones
- [ ] Implementar SubscriptionService
- [ ] Middleware de límites
- [ ] Página de planes
- [ ] Página de upgrade
- [ ] Dashboard de suscripción

### Semana 3: Multimedia
- [ ] Implementar AudioHandler
- [ ] Mejorar ImageProcessor
- [ ] Integrar con message_handler
- [ ] Probar transcripción
- [ ] Probar TTS
- [ ] Probar análisis de imágenes

---

*Continúa en siguientes fases...*
