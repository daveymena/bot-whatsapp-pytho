"""
Script para verificar la instalación del sistema SaaS
"""
import sys
import os

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    dependencies = {
        'openai': 'OpenAI API',
        'gtts': 'Google Text-to-Speech',
        'pytesseract': 'Tesseract OCR',
        'PIL': 'Pillow (Procesamiento de imágenes)'
    }
    
    missing = []
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - NO INSTALADO")
            missing.append(module)
    
    return len(missing) == 0

def check_database():
    """Verifica las tablas de la base de datos"""
    print("\n🔍 Verificando base de datos...")
    
    try:
        from database.models import (
            SubscriptionPlan, Subscription, PaymentHistory,
            UsageMetrics, VerificationCode, License
        )
        from database.connection import SessionLocal
        
        db = SessionLocal()
        
        # Verificar planes
        plans_count = db.query(SubscriptionPlan).count()
        print(f"  ✅ Planes de suscripción: {plans_count}")
        
        if plans_count > 0:
            plans = db.query(SubscriptionPlan).all()
            for plan in plans:
                print(f"     - {plan.name}: ${plan.price_monthly:,.0f}/mes")
        
        # Verificar suscripciones
        subs_count = db.query(Subscription).count()
        print(f"  ✅ Suscripciones activas: {subs_count}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def check_env_variables():
    """Verifica las variables de entorno"""
    print("\n🔍 Verificando configuración (.env)...")
    
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API Key',
        'SMTP_USER': 'Email SMTP',
        'SMTP_PASSWORD': 'Contraseña SMTP',
    }
    
    optional_vars = {
        'TTS_ENABLED': 'Text-to-Speech',
        'VISION_AI_ENABLED': 'Vision AI',
        'OCR_ENABLED': 'OCR',
    }
    
    missing = []
    for var, name in required_vars.items():
        value = os.getenv(var)
        if value:
            # Ocultar parte del valor por seguridad
            masked = value[:4] + '...' + value[-4:] if len(value) > 8 else '***'
            print(f"  ✅ {name}: {masked}")
        else:
            print(f"  ⚠️  {name}: NO CONFIGURADO")
            missing.append(var)
    
    for var, name in optional_vars.items():
        value = os.getenv(var, 'false')
        status = "✅" if value.lower() == 'true' else "⚠️"
        print(f"  {status} {name}: {value}")
    
    return len(missing) == 0

def check_tesseract():
    """Verifica que Tesseract esté instalado"""
    print("\n🔍 Verificando Tesseract OCR...")
    
    try:
        import pytesseract
        from PIL import Image
        
        # Intentar obtener la versión
        version = pytesseract.get_tesseract_version()
        print(f"  ✅ Tesseract instalado: v{version}")
        return True
        
    except Exception as e:
        print(f"  ❌ Tesseract no encontrado")
        print(f"     Instala desde: https://github.com/UB-Mannheim/tesseract/wiki")
        return False

def check_services():
    """Verifica que los servicios estén disponibles"""
    print("\n🔍 Verificando servicios...")
    
    services = [
        ('whatsapp.audio_handler', 'AudioHandler', 'Procesamiento de Audio'),
        ('whatsapp.image_processor', 'ImageProcessor', 'Procesamiento de Imágenes'),
        ('services.subscription_service', 'SubscriptionService', 'Sistema de Suscripciones'),
        ('services.email_service', 'EmailService', 'Servicio de Email'),
    ]
    
    all_ok = True
    for module_name, class_name, description in services:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  ✅ {description}")
        except Exception as e:
            print(f"  ❌ {description}: {e}")
            all_ok = False
    
    return all_ok

def main():
    """Ejecuta todas las verificaciones"""
    print("=" * 50)
    print("  VERIFICACIÓN DEL SISTEMA SAAS")
    print("=" * 50)
    print()
    
    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    results = {
        'Dependencias': check_dependencies(),
        'Base de Datos': check_database(),
        'Variables de Entorno': check_env_variables(),
        'Tesseract OCR': check_tesseract(),
        'Servicios': check_services(),
    }
    
    print("\n" + "=" * 50)
    print("  RESUMEN")
    print("=" * 50)
    
    for check, passed in results.items():
        status = "✅ CORRECTO" if passed else "❌ REQUIERE ATENCIÓN"
        print(f"{check}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ ¡SISTEMA LISTO PARA USAR!")
        print("\nInicia el sistema con: START_SYSTEM.bat")
    else:
        print("⚠️  CONFIGURACIÓN INCOMPLETA")
        print("\nRevisa INSTALACION_EXITOSA.md para más detalles")
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
