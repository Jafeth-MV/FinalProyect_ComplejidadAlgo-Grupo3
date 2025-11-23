# 🚀 CÓMO EJECUTAR RUTAFIX - GUÍA RÁPIDA

## Comandos para Ejecutar el Proyecto

### OPCIÓN 1: Ejecutar la Aplicación Web (RECOMENDADO)

#### Paso 1: Abrir Terminal/PowerShell
```powershell
# Presiona Win + R, escribe "powershell" y Enter
```

#### Paso 2: Navegar a la carpeta Front
```powershell
cd C:\Users\Jafeth\IdeaProjects\FinalProyect_ComplejidadAlgo-Grupo3\Front
```

#### Paso 3: Instalar dependencias (solo la primera vez)
```powershell
pip install -r requirements.txt
```

#### Paso 4: Ejecutar el servidor
```powershell
python app.py
```

**✅ Resultado:**
- El servidor se iniciará en el puerto 5000
- Abre tu navegador en: **http://localhost:5000**
- Verás la interfaz web de RutaFix

#### Para detener el servidor:
```powershell
# Presiona Ctrl + C en la terminal
```

---

### OPCIÓN 2: Ejecutar Scripts de Hito-2 (Python Standalone)

#### Paso 1: Navegar a Hito-2
```powershell
cd C:\Users\Jafeth\IdeaProjects\FinalProyect_ComplejidadAlgo-Grupo3\Hito-2
```

#### Paso 2: Instalar dependencias (solo la primera vez)
```powershell
pip install -r requirements.txt
```

#### Paso 3: Ejecutar el script principal
```powershell
python main.py
```

**✅ Resultado:**
- Ejecuta optimización de rutas
- Genera archivos JSON con resultados
- Crea imágenes PNG con visualizaciones
- Muestra análisis en consola

---

### OPCIÓN 3: Ejecutar Tests de la API

#### Asegúrate que el servidor esté corriendo primero (app.py)

```powershell
# En otra terminal, navega a Front
cd C:\Users\Jafeth\IdeaProjects\FinalProyect_ComplejidadAlgo-Grupo3\Front

# Ejecuta los tests
python test_api.py
```

**✅ Resultado:**
- Ejecuta 7 pruebas automáticas
- Muestra resultados: ✓ PASS o ✗ FAIL
- Resumen al final

---

## 📋 Comandos Útiles

### Ver si el servidor está corriendo
```powershell
# Verificar procesos Python activos
Get-Process | Where-Object {$_.ProcessName -eq "python"}
```

### Detener todos los servidores Python
```powershell
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process -Force
```

### Verificar puerto 5000 en uso
```powershell
netstat -ano | findstr :5000
```

### Reinstalar dependencias
```powershell
cd Front
pip install -r requirements.txt --force-reinstall
```

---

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError"
```powershell
# Reinstalar dependencias
cd Front
pip install -r requirements.txt
```

### Error: "Puerto 5000 en uso"
```powershell
# Detener proceso en puerto 5000
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force
```

### Error: "pip no se reconoce"
```powershell
# Usar Python directamente
python -m pip install -r requirements.txt
```

---

## 🌐 URLs Importantes

- **Aplicación Web:** http://localhost:5000
- **Alternativa:** http://127.0.0.1:5000

---

## 📁 Estructura de Carpetas

```
FinalProyect_ComplejidadAlgo-Grupo3/
├── Front/              ← Aplicación web principal
│   ├── app.py         ← Ejecutar este archivo
│   └── requirements.txt
│
└── Hito-2/            ← Scripts Python
    ├── main.py        ← Ejecutar este archivo
    └── requirements.txt
```

---

## ⚡ COMANDO RÁPIDO (Copiar y Pegar)

### Para ejecutar la aplicación web:
```powershell
cd C:\Users\Jafeth\IdeaProjects\FinalProyect_ComplejidadAlgo-Grupo3\Front; python app.py
```

### Para ejecutar Hito-2:
```powershell
cd C:\Users\Jafeth\IdeaProjects\FinalProyect_ComplejidadAlgo-Grupo3\Hito-2; python main.py
```

### Para ejecutar tests:
```powershell
cd C:\Users\Jafeth\IdeaProjects\FinalProyect_ComplejidadAlgo-Grupo3\Front; python test_api.py
```

---

## 💡 Notas Importantes

1. **Siempre** ejecuta desde la carpeta correcta (Front o Hito-2)
2. **No cierres** la terminal mientras uses la aplicación web
3. **Instala dependencias** solo la primera vez o después de actualizaciones
4. **Usa Ctrl+C** para detener el servidor, no cierres la ventana directamente

---

**¡Listo para usar!** 🎉

