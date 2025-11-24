# 🚀 INICIO RÁPIDO - Sistema de Optimización con CSV

## ⚡ Ejecutar en 3 Pasos

### 1️⃣ Instalar Dependencias
```bash
pip install pandas numpy matplotlib scikit-learn geopy openpyxl flask
```

### 2️⃣ Elegir Modo de Ejecución

#### Opción A: Terminal (Más Rápido) 
```bash
cd Hito-2
python main.py
```
**✅ Genera:** `resultados_*.json` + `clusters_*.png`

#### Opción B: Frontend Web (Más Visual)
```bash
cd Front
python app.py
```
**✅ Accede a:** `http://localhost:5000`

### 3️⃣ Ver Resultados

- 📊 **JSON**: Datos completos de optimización
- 🖼️ **PNG**: Visualización de clusters y ruta
- 🗺️ **Mapa**: Interactivo en el frontend

---

## 📋 Lo Que Hace el Sistema

1. **Lee** el CSV de intervenciones viales → `1_Dataset_Intervenciones_PVD_30062025.csv`
2. **Genera** coordenadas automáticamente para cada ruta
3. **Agrupa** puntos cercanos con K-Means (5 clusters por defecto)
4. **Optimiza** cada cluster con TSP (algoritmo óptimo según tamaño)
5. **Conecta** clusters en el orden más eficiente
6. **Exporta** resultados y visualizaciones

---

## 🎯 Ejemplo de Salida

```
======================================================================
🚀 SISTEMA DE OPTIMIZACIÓN DE RUTAS DE EVACUACIÓN
======================================================================

📂 Cargando dataset desde CSV de intervenciones...
✓ CSV cargado con encoding latin1: 200 registros
✓ Generadas 25 ubicaciones desde el CSV

📊 Estadísticas del Dataset:
  - Puntos: 25
  - Latitud: [-18.3146, -16.1090]
  - Longitud: [-71.8375, -69.9502]

🔹 Clustering con K-Means...
✓ Clustering completado: 5 clusters

🔹 Resolviendo TSP para cada cluster...
  Cluster 0 (3 puntos): fuerza_bruta - 0.32 km - 0.0001s
  Cluster 1 (4 puntos): fuerza_bruta - 0.71 km - 0.0001s
  ...

📊 RESUMEN DE OPTIMIZACIÓN
============================================================
Puntos totales: 25
Clusters: 5
Distancia total: 13.38 km
Tiempo total: 2.96s
============================================================

📍 RUTA OPTIMIZADA:
  1. TA-101_JORGE BASADRE
  2. TA-515_CANDARAVE
  3. AR-119_AREQUIPA
  ...

✅ OPTIMIZACIÓN COMPLETADA
```

---

## 🎨 Frontend - Características

### Panel de Control
- 🗺️ **Base de Datos CSV** - Usa datos reales (RECOMENDADO)
- 📂 **Subir Archivo** - Excel o CSV personalizado
- 🎲 **Aleatorio** - Genera datos de prueba

### Configuración
- **Cantidad de Puntos**: 10-200 (50 por defecto)
- **Número de Clusters**: 1-10 (5 por defecto)

### Visualización
- **Mapa Interactivo**: Zoom, pan, marcadores
- **Clusters Coloreados**: Cada cluster con color único
- **Ruta Optimizada**: Líneas conectando puntos en orden
- **Lista de Puntos**: Secuencia completa de visita

### Estadísticas
- **Distancia Total**: En kilómetros
- **Tiempo de Ejecución**: En segundos
- **Distancia Intra-Clusters**: Dentro de cada grupo
- **Distancia Inter-Clusters**: Entre grupos

---

## 🔧 Ajustes Rápidos

### Cambiar Número de Puntos

**En Terminal:**
Edita `main.py` línea 146:
```python
MAX_PUNTOS = 50  # Cambiar aquí
```

**En Frontend:**
Usa el control deslizante en la interfaz

### Cambiar Número de Clusters

**En Terminal:**
Edita `main.py` línea 147:
```python
N_CLUSTERS = 5  # Cambiar aquí
```

**En Frontend:**
Usa el control deslizante en la interfaz

### Cambiar Método TSP

**En Terminal:**
Edita `main.py` línea 148:
```python
METODO_TSP = 'auto'  # Opciones: 'auto', 'fuerza_bruta', 'backtracking', 'vecino_cercano'
```

---

## ✅ Verificación Rápida

### ¿El sistema funciona?

```bash
cd Front
python test_csv.py
```

**Esperado:**
```
🧪 PRUEBA DE CARGA DEL CSV
✅ CSV cargado correctamente

🧪 PRUEBA DE OPTIMIZACIÓN
✅ Optimización completada

📊 RESUMEN DE PRUEBAS
✅ TODAS LAS PRUEBAS PASARON
```

---

## 📁 Archivos Importantes

```
📂 FinalProyect_ComplejidadAlgo-Grupo3/
│
├── 📄 RESUMEN_IMPLEMENTACION.md    ← TODO lo que se hizo
├── 📄 ACTUALIZACION_CSV.md         ← Cambios detallados
├── 📄 INICIO_RAPIDO.md             ← Este archivo
│
├── 📂 Hito-2/
│   ├── 📊 1_Dataset_Intervenciones_PVD_30062025.csv  ← DATOS
│   ├── 🐍 main.py                  ← EJECUTAR AQUÍ
│   └── 📄 README_CSV.md            ← Guía del CSV
│
└── 📂 Front/
    ├── 🐍 app.py                   ← EJECUTAR AQUÍ (Web)
    └── 🧪 test_csv.py              ← PROBAR AQUÍ
```

---

## 🐛 Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install pandas numpy matplotlib scikit-learn geopy openpyxl flask
```

### Error: "FileNotFoundError: CSV no encontrado"
Verifica que estás en la carpeta correcta:
```bash
cd Hito-2
dir 1_Dataset_Intervenciones_PVD_30062025.csv
```

### Frontend no carga
```bash
# 1. Verifica que Flask está corriendo
cd Front
python app.py

# 2. Accede a la URL correcta
http://localhost:5000
```

### El mapa no se muestra
- Verifica conexión a internet (usa CDN)
- Abre la consola del navegador (F12)
- Recarga la página (Ctrl+F5)

---

## 💡 Tips

1. **Usa el Frontend**: Es más visual y fácil de usar
2. **Empieza con pocos puntos**: 20-30 para pruebas rápidas
3. **Revisa las visualizaciones**: Los gráficos PNG son muy útiles
4. **Lee el JSON**: Contiene información detallada
5. **Prueba diferentes configuraciones**: Clusters, puntos, métodos

---

## 📚 Más Información

- `RESUMEN_IMPLEMENTACION.md` - Detalles técnicos completos
- `README_CSV.md` - Guía del CSV y coordenadas
- `ACTUALIZACION_CSV.md` - Cambios y mejoras

---

## 🎉 ¡Listo!

El sistema está **100% funcional** y listo para usar.

**Disfruta optimizando rutas! 🚀**

---

**Última actualización:** 23 de Noviembre, 2024

