# 🚀 Guía para Deployar RutaFix en Render

## ⚡ RESPUESTA RÁPIDA: ¿Necesito archivo .env?

**NO.** En Render configuras las variables de entorno directamente en el dashboard web. 

El archivo `.env` es solo para desarrollo local (tu computadora). **NUNCA lo subas a GitHub.**

---

## 📋 Archivos Necesarios (Ya Creados) ✅

- `requirements.txt` - Dependencias de Python
- `runtime.txt` - Versión de Python (3.11.0)
- `Procfile` - Comando para iniciar la app
- `.gitignore` - Ignora .env y otros archivos sensibles
- `.env.example` - Ejemplo de variables (NO se sube a producción)

---

## 🌐 Pasos para Deployar en Render

### Paso 1: Subir a GitHub

```bash
# Inicializar Git (si no lo has hecho)
git init

# Agregar archivos
git add .

# Commit
git commit -m "Preparar RutaFix para deploy"

# Crear repositorio en GitHub y conectarlo
git remote add origin https://github.com/TU_USUARIO/rutafix.git
git branch -M main
git push -u origin main
```

---

### Paso 2: Crear Web Service en Render

1. **Ve a [render.com](https://render.com)** e inicia sesión
2. Click en **"New +"** → **"Web Service"**
3. **Conecta tu repositorio** de GitHub
4. Selecciona el repositorio `rutafix`

---

### Paso 3: Configurar el Servicio

**Información Básica:**
- **Name:** `rutafix` (o el nombre que prefieras)
- **Region:** `Oregon (US West)` (o el más cercano)
- **Branch:** `main`
- **Root Directory:** *(dejar vacío)*

**Build & Deploy:**
- **Runtime:** `Python 3`
- **Build Command:** 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```bash
  cd Front && gunicorn app:app --bind 0.0.0.0:$PORT
  ```

---

### Paso 4: Configurar Variables de Entorno 🔑

**AQUÍ es donde configuras las variables** (sin necesidad de archivo .env):

En la sección **"Environment Variables"**, agrega:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `PYTHON_VERSION` | `3.11.0` |

**Render automáticamente proporciona:**
- `PORT` - Puerto asignado dinámicamente (no lo configures tú)

**Notas:**
- ✅ NO necesitas archivo .env
- ✅ Estas variables son seguras (no se ven en el código)
- ✅ Puedes cambiarlas sin hacer nuevo deploy

---

### Paso 5: Seleccionar Plan

- Selecciona **"Free"** (o el plan que prefieras)
- El plan gratuito incluye:
  - ✅ 750 horas/mes
  - ✅ SSL/HTTPS automático
  - ⚠️ La app "duerme" tras 15 min inactiva
  - ⚠️ Tarda ~30 seg en "despertar"

---

### Paso 6: Deploy 🚀

1. Click en **"Create Web Service"**
2. Render comenzará a:
   - Clonar tu repositorio
   - Instalar dependencias (`requirements.txt`)
   - Iniciar la aplicación
3. **Espera 5-10 minutos** ⏱️
4. ¡Listo! Tendrás una URL como: `https://rutafix.onrender.com`

---

## 📝 Desarrollo Local vs Producción

### En tu computadora (desarrollo):

1. **Crea un archivo `.env`** (copia de `.env.example`):
   ```bash
   cp Front/.env.example Front/.env
   ```

2. **Edita `.env`** con tus valores:
   ```
   FLASK_ENV=development
   FLASK_DEBUG=True
   PORT=5000
   ```

3. **Ejecuta la app:**
   ```bash
   cd Front
   python app.py
   ```

### En Render (producción):

- ❌ **NO subas** el archivo `.env` a GitHub
- ✅ **Configura** las variables en el dashboard de Render
- ✅ Render inyecta las variables automáticamente

---

## 🔐 Seguridad: ¿Qué NO subir a GitHub?

El archivo `.gitignore` ya está configurado para ignorar:
- ✅ `.env` (variables sensibles)
- ✅ `__pycache__/` (archivos temporales)
- ✅ `*.pyc` (bytecode de Python)
- ✅ `uploads/` (archivos subidos)

---

## 🐛 Solución de Problemas

### Error: "Application failed to respond"

**Causa:** El comando de inicio es incorrecto.

**Solución:** Verifica el Start Command:
```bash
cd Front && gunicorn app:app --bind 0.0.0.0:$PORT
```

---

### Error: "Module not found"

**Causa:** Falta alguna dependencia en `requirements.txt`.

**Solución:** Verifica que todas las librerías estén en `requirements.txt`:
```
Flask>=3.0.0
Flask-CORS>=4.0.0
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
geopy>=2.3.0
openpyxl>=3.1.0
python-dotenv>=1.0.0
folium>=0.14.0
gunicorn>=21.2.0
```

---

### Error: "Port already in use"

**Causa:** No estás usando la variable `$PORT` de Render.

**Solución:** Verifica que en `app.py` tengas:
```python
port = int(os.getenv('PORT', 5000))
```

---

### La app se inicia pero da error 404

**Causa:** Las rutas no están bien configuradas.

**Solución:** Verifica que la ruta raíz (`/`) esté definida en `routes/web.py`.

---

## 🔄 Actualizar la Aplicación Deployada

Cuando hagas cambios en tu código:

```bash
# Hacer cambios en tu código
git add .
git commit -m "Actualización: [describe tu cambio]"
git push origin main
```

**Render detectará automáticamente** los cambios y hará un **nuevo deploy automático**. ✅

---

## 📊 Monitoreo y Logs

En el dashboard de Render puedes:
- 📈 Ver métricas de uso (CPU, memoria)
- 📋 Ver logs en tiempo real
- 🔔 Configurar notificaciones por email
- 🔄 Ver historial de deploys
- 🛑 Detener/reiniciar el servicio

---

## 💡 Tips Importantes

1. **Primera carga lenta:** La primera vez que alguien accede, Render "despierta" la app (plan gratuito). Esto toma ~30 segundos.

2. **Mantener activa:** Si quieres que no "duerma", puedes usar servicios como UptimeRobot para hacer ping cada 10 minutos.

3. **Límite de tiempo:** El plan gratuito tiene límite de 750 horas/mes (≈31 días si la dejas corriendo 24/7).

4. **Base de datos:** Si necesitas base de datos, Render ofrece PostgreSQL gratuito (también configurable desde el dashboard).

---

## ✅ Checklist Final Antes de Deploy

Antes de hacer deploy, verifica:

- [ ] `requirements.txt` está en la raíz del proyecto
- [ ] `runtime.txt` especifica `python-3.11.0`
- [ ] `Procfile` tiene el comando correcto
- [ ] `.gitignore` incluye `.env`
- [ ] Código está en GitHub
- [ ] NO has subido archivos `.env` con claves sensibles
- [ ] El `app.py` usa `os.getenv('PORT', 5000)`
- [ ] El host es `0.0.0.0` (no `localhost`)

---

## 🎉 ¡Listo!

Una vez deployado, tu aplicación estará disponible en:
```
https://tu-app-name.onrender.com
```

Comparte ese enlace con quien quieras. **¡RutaFix estará en línea!** 🌐

---

## 📞 Ayuda Adicional

- **Documentación Render:** https://render.com/docs
- **Logs:** Dashboard → Tu servicio → "Logs"
- **Variables:** Dashboard → Tu servicio → "Environment"

---

**¿Problemas?** Revisa los logs en el dashboard de Render. La mayoría de errores se ven claramente ahí.

