# Solución al Error de Groq en Easypanel

## Problema
```
TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
```

Este error ocurre por un conflicto de versiones entre la librería `groq` y `httpx`.

## Solución

### 1. Actualizar requirements.txt
Ya se actualizó el archivo `requirements.txt` cambiando:
```
groq==0.4.2  ❌
```
Por:
```
groq>=0.11.0  ✅
```

### 2. Reconstruir la imagen en Easypanel

#### Opción A: Forzar rebuild completo
1. Ve a tu proyecto en Easypanel
2. Ve a la sección "Build"
3. Haz clic en "Rebuild" o "Force Rebuild"
4. Espera a que termine la construcción

#### Opción B: Hacer un nuevo commit
```bash
git add requirements.txt
git commit -m "fix: actualizar groq a version compatible"
git push
```

Easypanel detectará el cambio y reconstruirá automáticamente.

### 3. Verificar las variables de entorno
Asegúrate de que estas variables estén configuradas en Easypanel:

```
GROQ_API_KEY=tu_api_key_aqui
GROQ_API_KEY_2=tu_segunda_key (opcional)
GROQ_API_KEY_3=tu_tercera_key (opcional)
ENABLE_GROQ_ROTATION=true
GROQ_MODEL=llama-3.1-70b-versatile
GROQ_MAX_TOKENS=1000
```

### 4. Reiniciar el servicio
Después de la reconstrucción:
1. Ve a tu servicio en Easypanel
2. Haz clic en "Restart"
3. Verifica los logs para confirmar que inicia correctamente

## Verificación
Los logs deberían mostrar:
```
✅ Servidor iniciado en puerto 5000
✅ Base de datos conectada
✅ Sistema listo
```

En lugar de:
```
❌ TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
```

## Notas Adicionales

### ¿Por qué ocurrió esto?
- La versión `groq==0.4.2` es muy antigua (de principios de 2024)
- Las versiones nuevas de `httpx` (que groq usa internamente) cambiaron su API
- La versión `groq>=0.11.0` es compatible con las versiones actuales de httpx

### Versiones recomendadas
```
groq>=0.11.0        # Cliente de Groq actualizado
httpx>=0.25.0       # Se instala automáticamente como dependencia
```

## Comandos útiles para debugging

### Ver logs en tiempo real
En Easypanel, ve a la pestaña "Logs" de tu servicio.

### Verificar versión instalada
Si tienes acceso a la consola del contenedor:
```bash
pip show groq
pip show httpx
```

## Solución alternativa (si persiste el problema)

Si después de actualizar aún tienes problemas, puedes especificar versiones exactas:

```txt
groq==0.11.0
httpx==0.25.2
httpcore==1.0.2
```

Agrega estas líneas a `requirements.txt` y vuelve a hacer rebuild.
