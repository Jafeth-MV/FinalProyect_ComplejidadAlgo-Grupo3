# 🛑 Guía: Detener y Ejecutar Procesos

## Situación Actual
Tienes procesos corriendo (probablemente el frontend `sore` en Next.js)

---

## MÉTODO 1: Detener con Ctrl+C (MÁS RÁPIDO) ⚡

### Paso 1: Localiza la terminal donde está corriendo
- Busca la terminal que muestra mensajes como:
  - `✓ Ready in XXms`
  - `○ Compiling /...`
  - O que está "ocupada"

### Paso 2: Presiona Ctrl+C
```
Ctrl + C
```
- Esto detendrá el proceso inmediatamente
- Verás que recuperas el prompt (PS D:\... >)

---

## MÉTODO 2: Matar proceso específico desde PowerShell

### Ver qué procesos están corriendo:
```powershell
# Ver procesos Node.js
Get-Process | Where-Object {$_.ProcessName -like "*node*"}

# Ver procesos Python
Get-Process | Where-Object {$_.ProcessName -like "*python*"}
```

### Matar proceso por ID:
```powershell
# Reemplaza XXXX con el ID del proceso
Stop-Process -Id XXXX -Force
```

### Matar TODOS los procesos Node.js (cuidado):
```powershell
Get-Process node | Stop-Process -Force
```

### Matar TODOS los procesos Python (cuidado):
```powershell
Get-Process python | Stop-Process -Force
```

---

## MÉTODO 3: Cerrar la terminal

Simplemente cierra la ventana de la terminal donde está corriendo el proceso.

---

## 🚀 EJECUTAR HITO-2 (RECOMENDADO)

### Una vez detenido el proceso anterior:

```bash
# 1. Ir a la carpeta Hito-2
cd D:\WebstormProjects\Sistema-de-optimizacion-de-rutas-de-evacuacion\Hito-2

# 2. Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# 3. Ejecutar
python main.py
```

**Tiempo estimado:** 2-3 minutos

**Resultado:** 
- Verás progreso en consola
- Se generarán archivos:
  - `resultados_YYYYMMDD_HHMMSS.json`
  - `clusters_YYYYMMDD_HHMMSS.png`

---

## 🚀 EJECUTAR BACKEND (ALTERNATIVA)

```bash
# 1. Ir a la carpeta back
cd D:\WebstormProjects\Sistema-de-optimizacion-de-rutas-de-evacuacion\back

# 2. Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# 3. Ejecutar
python app.py
```

**Resultado:**
- Servidor corriendo en: http://localhost:5000
- Puedes probar con: http://localhost:5000/api/health

---

## 📝 COMANDOS RÁPIDOS

### Detener Node.js y ejecutar Hito-2:
```powershell
# Detener Node.js
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force

# Ejecutar Hito-2
cd D:\WebstormProjects\Sistema-de-optimizacion-de-rutas-de-evacuacion\Hito-2
pip install -r requirements.txt
python main.py
```

### Detener Node.js y ejecutar Backend:
```powershell
# Detener Node.js
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force

# Ejecutar Backend
cd D:\WebstormProjects\Sistema-de-optimizacion-de-rutas-de-evacuacion\back
pip install -r requirements.txt
python app.py
```

---

## ⚠️ IMPORTANTE

### Verificar que se detuvo:
```powershell
# Ver si aún hay procesos corriendo
Get-Process | Where-Object {$_.ProcessName -like "*node*"}

# Si no muestra nada = todo está detenido ✓
```

### Liberar puerto 3000 (si está ocupado):
```powershell
# Buscar qué usa el puerto 3000
netstat -ano | findstr :3000

# Matar proceso por ID (reemplaza XXXX)
Stop-Process -Id XXXX -Force
```

---

## 🎯 RECOMENDACIÓN

**Para ejecutar Hito-2 AHORA:**

1. **Presiona Ctrl+C** en la terminal donde está `npm run dev`
2. **Abre una nueva terminal** (o usa la misma)
3. **Ejecuta estos 3 comandos:**

```powershell
cd D:\WebstormProjects\Sistema-de-optimizacion-de-rutas-de-evacuacion\Hito-2
pip install -r requirements.txt
python main.py
```

**¡Eso es todo! 🎉**

---

## 💡 TIPS

- **Usar múltiples terminales:** Puedes tener Hito-2 y Backend corriendo al mismo tiempo en terminales diferentes
- **Ctrl+C siempre funciona:** Es la forma más limpia de detener procesos
- **WebStorm:** Puedes usar el terminal integrado de WebStorm (Alt+F12)

---

## 🆘 SI ALGO NO FUNCIONA

### Error: "Python no reconocido"
```powershell
python --version
# Si falla, instala Python 3.8+
```

### Error: "pip no reconocido"
```powershell
python -m pip install -r requirements.txt
```

### Error: "Archivo no encontrado"
```powershell
# Verifica que estás en la carpeta correcta
pwd
# Debe mostrar: ...\Sistema-de-optimizacion-de-rutas-de-evacuacion\Hito-2
```

---

**Última actualización:** 23/11/2025

