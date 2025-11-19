# 🚀 Solución Rápida - Errores de Base de Datos

## ❌ Problema Detectado

La base de datos no tiene las columnas nuevas necesarias para el sistema de pagos y fotos.

## ✅ Solución en 3 Pasos

### Paso 1: Ejecutar Migración

```bash
python migrate_database.py
```

O usar el script automático:

```bash
MIGRAR_BD.bat
```

### Paso 2: Verificar Migración

```bash
python test_payment_integration.py
```

### Paso 3: Iniciar Sistema

```bash
START_WITH_PAYMENTS.bat
```

## 📋 ¿Qué hace la migración?

La migración agrega las siguientes columnas:

### Tabla `products`:
- `image_url` - URL de la imagen principal
- `images` - Array JSON de imágenes adicionales
- `views` - Contador de vistas (para analytics)

### Tabla `orders`:
- `order_number` - Número único de orden (ORD-YYYYMMDD-XXXXXX)
- `payment_proof` - URL del comprobante de pago

### Índices:
- Índice en `products.image_url` para búsquedas rápidas
- Índice en `orders.order_number` para búsquedas rápidas
- Índice en `orders.payment_method` para analytics

## 🔍 Verificación Manual

Si quieres verificar manualmente que las columnas existan:

```sql
-- Verificar columnas de productos
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'products';

-- Verificar columnas de órdenes
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'orders';
```

## 📸 Agregar Imágenes a Productos

Después de la migración, agrega URLs reales de imágenes:

```python
from database.connection import SessionLocal
from database.models import Product

db = SessionLocal()

# Actualizar un producto
product = db.query(Product).filter(Product.id == 1).first()
product.image_url = "https://ejemplo.com/producto.jpg"
product.images = [
    "https://ejemplo.com/producto-1.jpg",
    "https://ejemplo.com/producto-2.jpg",
    "https://ejemplo.com/producto-3.jpg"
]

db.commit()
db.close()
```

## 🆘 Si la Migración Falla

### Error: "permission denied"

**Solución:** Asegúrate de tener permisos de ALTER TABLE en la base de datos.

```sql
-- Otorgar permisos (ejecutar como superusuario)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tu_usuario;
```

### Error: "relation does not exist"

**Solución:** Las tablas base no existen. Ejecuta primero:

```bash
python init_database.py
```

### Error: "column already exists"

**Solución:** Las columnas ya existen. Esto es normal, la migración las omitirá automáticamente.

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs de error
2. Verifica la conexión a la base de datos
3. Contacta: daveymena16@gmail.com

---

**Después de la migración, todo funcionará correctamente! 🎉**
