# 📸 SISTEMA DE FOTOS AUTOMÁTICAS

## ✅ IMPLEMENTADO

El bot ahora envía automáticamente las fotos de los productos cuando el cliente pregunta por ellos.

---

## 🎯 CÓMO FUNCIONA

### 1. Detección Automática
Cuando un cliente pregunta por un producto, el sistema:
- ✅ Busca productos relevantes en la base de datos
- ✅ Verifica si tienen fotos disponibles (`image_url` o `images`)
- ✅ Prepara las fotos para enviar automáticamente

### 2. Envío Inteligente
El bot envía fotos cuando:
- ✅ El cliente pregunta por un producto específico
- ✅ El cliente pide ver el catálogo
- ✅ El cliente dice "muéstrame", "quiero ver", "tienes fotos"
- ✅ El bot presenta un producto (etapa de presentación)

### 3. Formato del Mensaje
Cada foto incluye:
```
📸 *Nombre del Producto*

💰 *Precio:* $XX,XXX COP
📦 *Stock:* X unidades disponibles
📁 *Categoría:* Categoría del producto

Descripción breve del producto...
```

---

## 🔧 CONFIGURACIÓN

### Variables de Entorno (.env)
```env
# Habilitar envío automático de fotos
SMART_PHOTOS_ENABLED=true
AUTO_SEND_PHOTOS=true

# Máximo de fotos por producto
SMART_PHOTOS_MAX_PER_PRODUCT=3

# Directorio temporal para fotos
SMART_PHOTOS_TEMP_DIR=./temp-images
```

---

## 📝 EJEMPLOS DE USO

### Ejemplo 1: Cliente pregunta por producto
```
Cliente: "Hola, tienes cursos de Excel?"

Bot: "👋 ¡Hola! Sí, tengo cursos de Excel disponibles.

📸 Te envío la información con foto:

[FOTO DEL CURSO]

📸 *Curso de Excel Avanzado*

💰 *Precio:* $49,000 COP
📦 *Stock:* 15 unidades disponibles
📁 *Categoría:* Cursos Digitales

Aprende Excel desde cero hasta nivel avanzado...

¿Te interesa este curso? 😊"
```

### Ejemplo 2: Cliente pide ver catálogo
```
Cliente: "Muéstrame lo que tienes"

Bot: "¡Perfecto! Te muestro nuestros productos disponibles 📸

[FOTO 1]
📸 *Curso de Excel Avanzado*
💰 $49,000 COP

[FOTO 2]
📸 *Audífonos Bluetooth*
💰 $89,000 COP

[FOTO 3]
📸 *Mouse Inalámbrico*
💰 $35,000 COP

¿Cuál te interesa más? 😊"
```

### Ejemplo 3: Producto sin foto
```
Cliente: "Tienes el curso de Python?"

Bot: "Sí, tengo el curso de Python disponible.

📄 *Curso de Python Básico*
💰 $59,000 COP
📦 15 unidades disponibles

⚠️ Actualmente no tengo la foto disponible en el sistema.

¿Te gustaría que:
1️⃣ Te envíe más información del curso
2️⃣ Te muestre cursos similares con fotos
3️⃣ Te contacte con un asesor

¿Qué prefieres? 😊"
```

---

## 🎨 CARACTERÍSTICAS

### ✅ Envío Automático
- El bot detecta automáticamente cuando debe enviar fotos
- No necesitas pedirle explícitamente que envíe fotos
- Funciona desde la primera pregunta del cliente

### ✅ Múltiples Fotos
- Envía hasta 3 fotos por producto (configurable)
- Foto principal + fotos adicionales
- Cada foto con su descripción

### ✅ Indicadores Visuales
- 📸 = Producto con foto disponible
- 📄 = Producto sin foto disponible
- ✅ = Foto disponible
- ⚠️ = Sin foto disponible

### ✅ Manejo Inteligente
- Si no hay foto, ofrece alternativas
- Si hay múltiples productos, envía los más relevantes
- Prioriza productos con fotos disponibles

---

## 🔍 VERIFICAR PRODUCTOS CON FOTOS

### Consulta SQL
```sql
-- Ver productos con fotos
SELECT id, name, price, image_url 
FROM products 
WHERE image_url IS NOT NULL;

-- Contar productos con fotos
SELECT COUNT(*) as total_con_fotos 
FROM products 
WHERE image_url IS NOT NULL;
```

### Script Python
```python
from database.connection import SessionLocal
from database.models import Product

db = SessionLocal()

# Productos con fotos
products_with_photos = db.query(Product).filter(
    Product.image_url.isnot(None)
).all()

print(f"Productos con fotos: {len(products_with_photos)}")

for p in products_with_photos:
    print(f"- {p.name}: {p.image_url}")

db.close()
```

---

## 📦 AGREGAR FOTOS A PRODUCTOS

### Opción 1: Desde el Dashboard
1. Ir a "Productos"
2. Editar producto
3. Agregar URL de la foto en "image_url"
4. Guardar

### Opción 2: Desde la Base de Datos
```sql
-- Agregar foto a un producto
UPDATE products 
SET image_url = 'https://ejemplo.com/foto.jpg'
WHERE id = 1;

-- Agregar múltiples fotos
UPDATE products 
SET images = '["https://ejemplo.com/foto1.jpg", "https://ejemplo.com/foto2.jpg"]'::json
WHERE id = 1;
```

### Opción 3: Desde Python
```python
from database.connection import SessionLocal
from database.models import Product

db = SessionLocal()

# Actualizar foto de un producto
product = db.query(Product).filter_by(id=1).first()
product.image_url = "https://ejemplo.com/foto.jpg"
product.images = ["https://ejemplo.com/foto1.jpg", "https://ejemplo.com/foto2.jpg"]

db.commit()
db.close()
```

---

## 🚀 INTEGRACIÓN CON WHATSAPP

El sistema está preparado para enviar fotos a través de:

### Baileys (WhatsApp Web)
```javascript
// El handler de Python envía:
{
  text: "Mensaje del bot",
  photos: [
    {
      photos: ["url1.jpg", "url2.jpg"],
      caption: "Descripción del producto",
      product_id: 1,
      product_name: "Nombre del producto"
    }
  ]
}

// Baileys procesa y envía las fotos
await sock.sendMessage(phone, {
  image: { url: photo_url },
  caption: caption
});
```

---

## ⚠️ SOLUCIÓN DE PROBLEMAS

### Problema: "No tiene foto del curso"
**Causa:** El producto no tiene `image_url` en la base de datos

**Solución:**
```sql
-- Verificar si el producto tiene foto
SELECT id, name, image_url FROM products WHERE name LIKE '%curso%';

-- Si no tiene, agregar foto
UPDATE products 
SET image_url = 'https://ejemplo.com/curso.jpg'
WHERE id = X;
```

### Problema: El bot no envía fotos automáticamente
**Causa:** Variable de entorno deshabilitada

**Solución:**
```env
# Verificar en .env
AUTO_SEND_PHOTOS=true
SMART_PHOTOS_ENABLED=true
```

### Problema: Las fotos no se muestran
**Causa:** URL de foto inválida o no accesible

**Solución:**
- Verificar que la URL sea pública y accesible
- Usar URLs de servicios confiables (Cloudinary, AWS S3, etc.)
- Verificar que la URL termine en .jpg, .png, .webp

---

## 📊 ESTADÍSTICAS

Para ver cuántos productos tienen fotos:

```python
from database.connection import SessionLocal
from database.models import Product

db = SessionLocal()

total = db.query(Product).count()
with_photos = db.query(Product).filter(Product.image_url.isnot(None)).count()
without_photos = total - with_photos

print(f"Total productos: {total}")
print(f"Con fotos: {with_photos} ({with_photos/total*100:.1f}%)")
print(f"Sin fotos: {without_photos} ({without_photos/total*100:.1f}%)")

db.close()
```

---

## ✅ CONCLUSIÓN

El sistema de fotos automáticas está completamente implementado y funcionando. El bot ahora:

✅ Detecta automáticamente cuando enviar fotos
✅ Envía fotos desde la primera pregunta del cliente
✅ Maneja productos con y sin fotos inteligentemente
✅ Ofrece alternativas cuando no hay fotos disponibles

**El bot siempre enviará fotos cuando estén disponibles en la base de datos.**
