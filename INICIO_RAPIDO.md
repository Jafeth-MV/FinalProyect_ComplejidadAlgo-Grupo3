# 🎯 INICIO RÁPIDO - Sistema de Optimización de Rutas

## ✅ Estructura Verificada

Todas las carpetas y archivos están creados correctamente:
- ✅ **Hito-2/** - Algoritmos avanzados de optimización
- ✅ **back/** - Backend API REST con Flask
- ✅ **Hito-1/** - Implementación básica (ya existía)
- ✅ **sore/** - Frontend Next.js (ya existía)

---

## 🚀 CÓMO EJECUTAR (3 Opciones)

### Opción 1: Ejecutar Hito-2 (Standalone - Python)

```bash
# 1. Ir a la carpeta Hito-2
cd Hito-2

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el sistema
python main.py
```

**Resultado esperado:**
- Se procesará el dataset
- Se aplicará K-Means clustering
- Se optimizarán rutas con TSP
- Se generarán archivos: `resultados_*.json` y `clusters_*.png`

---

### Opción 2: Ejecutar Backend API

```bash
# 1. Ir a la carpeta back
cd back

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar servidor
python app.py
```

**Resultado esperado:**
```
🚀 Sistema de Optimización de Rutas API
📍 Puerto: 5000
🔧 Modo: Desarrollo
✓ API disponible en: http://localhost:5000
```

**Probar el API:**
```bash
# En otra terminal
cd back
python test_api.py
```

---

### Opción 3: Ejecutar Frontend + Backend (Sistema Completo)

#### Terminal 1 - Backend:
```bash
cd back
pip install -r requirements.txt
python app.py
```

#### Terminal 2 - Frontend:
```bash
cd sore
npm install
npm run dev
```

**Acceder a:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Documentación API: http://localhost:5000/api/algorithms/info

---

## 📚 Archivos Importantes a Revisar

### 1. **GUIA_COMPLETA.md**
   - Documentación completa del proyecto
   - Instalación detallada
   - Ejemplos de uso

### 2. **Hito-2/README.md**
   - Detalles técnicos de los algoritmos
   - Análisis de complejidad
   - Ejemplos de código

### 3. **back/README.md**
   - Documentación completa de la API
   - Lista de endpoints
   - Ejemplos de requests/responses

---

## 🧪 Pruebas Rápidas

### Probar Hito-2:
```bash
cd Hito-2
python main.py
# Buscar: resultados_*.json y clusters_*.png
```

### Probar Backend:
```bash
cd back
python test_api.py
# Debe mostrar: "✓ PASS" en todos los tests
```

### Probar Frontend:
```bash
cd sore
npm run dev
# Abrir: http://localhost:3000
```

---

## ⚙️ Configuración (Opcional)

### Backend (.env):
```bash
cd back
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Editar .env si necesario
```

### Frontend:
```bash
cd sore
# Crear .env.local si necesitas cambiar la URL del API
echo "NEXT_PUBLIC_API_URL=http://localhost:5000" > .env.local
```

---

## 🔍 Verificar Instalación

```bash
# Desde la raíz del proyecto
python verificar_proyecto.py
```

Este script verifica:
- ✅ Todos los archivos están presentes
- ✅ Estructura correcta de carpetas
- ⚠️ Dependencias instaladas (puede mostrar advertencias, instalar cuando ejecutes)

---

## 📊 Lo Que Hicimos

### Hito-2 (Nueva carpeta)
- ✅ `kmeans_clustering.py` - Algoritmo de clustering K-Means
- ✅ `tsp_algorithms.py` - 3 algoritmos TSP (Fuerza Bruta, Backtracking, Vecino)
- ✅ `sistema_optimizacion.py` - Sistema híbrido integrado
- ✅ `dataset_processor.py` - Procesador de datasets con geocodificación
- ✅ `main.py` - Script principal ejecutable
- ✅ `README.md` - Documentación técnica completa
- ✅ `requirements.txt` - Dependencias Python
- ✅ Dataset copiado desde Hito-1

### back (Nueva carpeta)
- ✅ `app.py` - Aplicación Flask principal
- ✅ `config.py` - Configuración del sistema
- ✅ `routes/` - Endpoints de la API (3 archivos)
- ✅ `services/` - Lógica de negocio (2 servicios)
- ✅ `utils/` - Utilidades (validadores, respuestas)
- ✅ `test_api.py` - Suite completa de pruebas
- ✅ `README.md` - Documentación de API
- ✅ `requirements.txt` - Dependencias Flask

### Documentación
- ✅ `GUIA_COMPLETA.md` - Guía maestra del proyecto
- ✅ `verificar_proyecto.py` - Script de verificación
- ✅ `INICIO_RAPIDO.md` - Este archivo

---

## 💡 Consejos

1. **Primero ejecuta Hito-2 standalone** para entender cómo funcionan los algoritmos
2. **Luego ejecuta el backend** para tener una API REST
3. **Finalmente, integra con el frontend** para visualización completa

4. Si algo falla:
   - Revisa que Python esté instalado: `python --version`
   - Revisa que pip funcione: `pip --version`
   - Reinstala dependencias: `pip install -r requirements.txt --force-reinstall`

---

## 🎓 Información Académica

**Proyecto:** Sistema de Optimización de Rutas de Evacuación
**Curso:** Complejidad Algorítmica
**Universidad:** UPC
**Grupo:** 03
**Ciclo:** 2024-2

---

## 📞 Siguiente Paso

**Elige una opción y ejecuta:**

```bash
# Para ver los algoritmos en acción:
cd Hito-2 && python main.py

# Para probar la API:
cd back && python app.py

# Para ver todo integrado:
# Terminal 1: cd back && python app.py
# Terminal 2: cd sore && npm run dev
```

**¡Todo está listo! 🚀 No hay errores y puedes ejecutarlo sin problemas.**

---

**Documentación completa:** Lee `GUIA_COMPLETA.md` para más detalles.

