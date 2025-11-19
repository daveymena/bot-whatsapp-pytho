"""
Email Service - Envío de emails (verificación, recuperación, notificaciones)
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_user)
        self.from_name = os.getenv('FROM_NAME', 'Bot WhatsApp')
        
        self.enabled = bool(self.smtp_user and self.smtp_password)
        
        if not self.enabled:
            logger.warning("Email service not configured. Set SMTP_USER and SMTP_PASSWORD in .env")
    
    def generate_code(self, length=6):
        """Generar código de verificación"""
        return ''.join(random.choices(string.digits, k=length))
    
    async def send_verification_email(self, email: str, code: str, name: str = None):
        """Enviar email de verificación"""
        subject = "Verifica tu email - Bot WhatsApp"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0;">Bot WhatsApp</h1>
            </div>
            
            <div style="padding: 30px; background-color: #f9fafb;">
                <h2 style="color: #1f2937;">¡Hola{' ' + name if name else ''}!</h2>
                <p style="color: #4b5563; font-size: 16px;">
                    Gracias por registrarte. Para completar tu registro, por favor verifica tu email.
                </p>
                
                <div style="background-color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 30px 0;">
                    <p style="color: #6b7280; margin-bottom: 10px;">Tu código de verificación es:</p>
                    <h1 style="color: #667eea; font-size: 48px; margin: 10px 0; letter-spacing: 8px;">{code}</h1>
                    <p style="color: #9ca3af; font-size: 14px;">Este código expira en 15 minutos</p>
                </div>
                
                <p style="color: #6b7280; font-size: 14px;">
                    Si no solicitaste este código, puedes ignorar este email.
                </p>
            </div>
            
            <div style="background-color: #1f2937; padding: 20px; text-align: center;">
                <p style="color: #9ca3af; font-size: 12px; margin: 0;">
                    © 2025 Bot WhatsApp. Todos los derechos reservados.
                </p>
            </div>
        </body>
        </html>
        """
        
        return await self._send_email(email, subject, body)

    
    async def send_password_reset_email(self, email: str, code: str, name: str = None):
        """Enviar email de recuperación de contraseña"""
        subject = "Recupera tu contraseña - Bot WhatsApp"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0;">Recuperación de Contraseña</h1>
            </div>
            
            <div style="padding: 30px; background-color: #f9fafb;">
                <h2 style="color: #1f2937;">¡Hola{' ' + name if name else ''}!</h2>
                <p style="color: #4b5563; font-size: 16px;">
                    Recibimos una solicitud para restablecer tu contraseña.
                </p>
                
                <div style="background-color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 30px 0;">
                    <p style="color: #6b7280; margin-bottom: 10px;">Tu código de recuperación es:</p>
                    <h1 style="color: #f5576c; font-size: 48px; margin: 10px 0; letter-spacing: 8px;">{code}</h1>
                    <p style="color: #9ca3af; font-size: 14px;">Este código expira en 15 minutos</p>
                </div>
                
                <p style="color: #6b7280; font-size: 14px;">
                    Si no solicitaste restablecer tu contraseña, ignora este email y tu contraseña permanecerá sin cambios.
                </p>
            </div>
            
            <div style="background-color: #1f2937; padding: 20px; text-align: center;">
                <p style="color: #9ca3af; font-size: 12px; margin: 0;">
                    © 2025 Bot WhatsApp. Todos los derechos reservados.
                </p>
            </div>
        </body>
        </html>
        """
        
        return await self._send_email(email, subject, body)
    
    async def send_welcome_email(self, email: str, name: str):
        """Enviar email de bienvenida"""
        subject = "¡Bienvenido a Bot WhatsApp!"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0;">¡Bienvenido!</h1>
            </div>
            
            <div style="padding: 30px; background-color: #f9fafb;">
                <h2 style="color: #1f2937;">¡Hola {name}!</h2>
                <p style="color: #4b5563; font-size: 16px;">
                    Gracias por unirte a Bot WhatsApp. Estamos emocionados de tenerte con nosotros.
                </p>
                
                <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 30px 0;">
                    <h3 style="color: #667eea;">Primeros pasos:</h3>
                    <ul style="color: #4b5563; line-height: 1.8;">
                        <li>Conecta tu WhatsApp</li>
                        <li>Agrega tus productos</li>
                        <li>Configura tu bot</li>
                        <li>¡Empieza a vender!</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:3000/dashboard" 
                       style="background-color: #667eea; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 6px; display: inline-block;">
                        Ir al Dashboard
                    </a>
                </div>
            </div>
            
            <div style="background-color: #1f2937; padding: 20px; text-align: center;">
                <p style="color: #9ca3af; font-size: 12px; margin: 0;">
                    © 2025 Bot WhatsApp. Todos los derechos reservados.
                </p>
            </div>
        </body>
        </html>
        """
        
        return await self._send_email(email, subject, body)
    
    async def send_subscription_confirmation(self, email: str, name: str, plan_name: str, amount: float):
        """Enviar confirmación de suscripción"""
        subject = f"Suscripción confirmada - Plan {plan_name}"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0;">¡Suscripción Confirmada!</h1>
            </div>
            
            <div style="padding: 30px; background-color: #f9fafb;">
                <h2 style="color: #1f2937;">¡Hola {name}!</h2>
                <p style="color: #4b5563; font-size: 16px;">
                    Tu suscripción al plan <strong>{plan_name}</strong> ha sido confirmada.
                </p>
                
                <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 30px 0;">
                    <h3 style="color: #11998e;">Detalles de tu suscripción:</h3>
                    <table style="width: 100%; color: #4b5563;">
                        <tr>
                            <td style="padding: 10px 0;"><strong>Plan:</strong></td>
                            <td style="text-align: right;">{plan_name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px 0;"><strong>Monto:</strong></td>
                            <td style="text-align: right;">${amount:,.0f} COP</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px 0;"><strong>Fecha:</strong></td>
                            <td style="text-align: right;">{datetime.now().strftime('%d/%m/%Y')}</td>
                        </tr>
                    </table>
                </div>
                
                <p style="color: #6b7280; font-size: 14px;">
                    Gracias por confiar en nosotros. ¡Disfruta de todas las funcionalidades!
                </p>
            </div>
            
            <div style="background-color: #1f2937; padding: 20px; text-align: center;">
                <p style="color: #9ca3af; font-size: 12px; margin: 0;">
                    © 2025 Bot WhatsApp. Todos los derechos reservados.
                </p>
            </div>
        </body>
        </html>
        """
        
        return await self._send_email(email, subject, body)
    
    async def _send_email(self, to_email: str, subject: str, html_body: str):
        """Enviar email (método interno)"""
        if not self.enabled:
            logger.warning(f"Email not sent (service disabled): {subject} to {to_email}")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully: {subject} to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
