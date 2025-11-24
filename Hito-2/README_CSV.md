# 📊 Sistema de Optimización de Rutas - Uso con Base de Datos CSV

## 🎯 Descripción

Este sistema utiliza la base de datos **`1_Dataset_Intervenciones_PVD_30062025.csv`** para generar rutas optimizadas usando algoritmos de clustering (K-Means) y TSP (Traveling Salesman Problem).

## 📁 Estructura de la Base de Datos CSV

El archivo CSV contiene información de intervenciones viales en Perú con las siguientes columnas clave:

- **CODIGO_RUTA**: Código único de la ruta (ej: TA-101, AR-119)
- **DEPARTAMENTO**: Departamento del Perú donde se ubica la intervención
- **PROVINCIA**: Provincia específica
- **INICIO / FINAL**: Kilometraje de inicio y fin de la intervención
- **LONGITUD**: Longitud de la intervención en kilómetros
- **ESTADO**: Estado de la vía (BUENO, REGULAR, MALO)
- **SUPERFICIE**: Tipo de superficie (ASFALTADO, SOLUCION BASICA, etc.)

## 🚀 Cómo Funciona

### 1. Generación de Coordenadas

El sistema **automáticamente** genera coordenadas geográficas basándose en:
- **Coordenadas de capitales departamentales** (predefinidas)
- **Variación aleatoria** para distribuir puntos dentro de cada departamento
- **Datos de rutas únicas** del CSV

### 2. Proceso de Optimización

```
CSV → Generación de Coordenadas → K-Means Clustering → TSP por Cluster → Ruta Optimizada
```

#### Algoritmos Utilizados:

1. **K-Means Clustering**: Agrupa puntos cercanos geográficamente
2. **TSP (Fuerza Bruta)**: Para clusters pequeños (≤10 puntos)
3. **TSP (Backtracking)**: Para clusters medianos (≤15 puntos)
4. **TSP (Vecino Cercano)**: Para clusters grandes (>15 puntos)

## 💻 Uso del Sistema

### Opción 1: Ejecución Directa

```bash
cd Hito-2
python main.py
```

El sistema automáticamente:
1. ✅ Busca `dataset_tp_complejidad.xlsx`
2. ✅ Si no existe, carga `1_Dataset_Intervenciones_PVD_30062025.csv`
3. ✅ Genera coordenadas automáticamente
4. ✅ Ejecuta la optimización
5. ✅ Genera visualizaciones y archivos de resultados

### Opción 2: Ejecución con Flask (API Web)

```bash
cd Hito-2
python app.py
```

Luego accede a: `http://localhost:5000/optimizar`

### Opción 3: Frontend Completo

```bash
cd Front
python app.py
```

Luego accede a: `http://localhost:5001`

## 📊 Archivos Generados

Después de la ejecución, se generan:

### 1. Resultados JSON
```
resultados_YYYYMMDD_HHMMSS.json
```
Contiene:
- Ruta global optimizada
- Información de clusters
- Estadísticas de distancias y tiempos
- Complejidad algorítmica

### 2. Visualización PNG
```
clusters_YYYYMMDD_HHMMSS.png
```
Muestra:
- **Panel izquierdo**: Clusters K-Means con centros
- **Panel derecho**: Ruta optimizada completa

## 🔧 Configuración

Puedes modificar parámetros en `main.py`:

```python
MAX_PUNTOS = 50        # Número máximo de puntos a procesar
N_CLUSTERS = 5         # Número de clusters para K-Means
METODO_TSP = 'auto'    # Método TSP: 'auto', 'fuerza_bruta', 'backtracking', 'vecino_cercano'
```

## 📈 Análisis de Complejidad

### Sin Optimización (TSP Directo)
- **50 puntos**: O(50!) ≈ 3.04×10⁶⁴ operaciones ❌ **INTRATABLE**

### Con Optimización Híbrida (K-Means + TSP)
- **5 clusters de ~10 puntos cada uno**
- **Complejidad por cluster**: O(10!) ≈ 3,628,800 operaciones
- **Complejidad total**: O(5 × 10!) ≈ 18,144,000 operaciones ✅ **VIABLE**

### Reducción de Complejidad
```
Reducción: ~10⁵⁸ veces más eficiente
```

## 🗺️ Departamentos Soportados

El sistema incluye coordenadas para todos los departamentos del Perú:

- Amazonas, Ancash, Apurímac, Arequipa
- Ayacucho, Cajamarca, Cusco
- Huancavelica, Huánuco
- Ica, Junín
- La Libertad, Lambayeque, Lima, Loreto
- Madre de Dios, Moquegua
- Pasco, Piura, Puno
- San Martín
- Tacna, Tumbes
- Ucayali

## 📋 Ejemplo de Salida

```
======================================================================
🚀 SISTEMA DE OPTIMIZACIÓN DE RUTAS DE EVACUACIÓN
======================================================================
Algoritmos: K-Means + TSP (Fuerza Bruta/Backtracking/Vecino Cercano)
======================================================================

📂 Cargando dataset desde CSV de intervenciones...
✓ CSV cargado con encoding latin1: 200 registros
✓ Generadas 25 ubicaciones desde el CSV

📊 Estadísticas del Dataset:
  - Puntos: 25
  - Latitud: [-18.3146, -16.1090]
  - Longitud: [-71.8375, -69.9502]

======================================================================
🔧 CONFIGURACIÓN DE OPTIMIZACIÓN
======================================================================
Clusters: 5
Método TSP: auto
======================================================================

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
======================================================================
  1. Ruta_0_TA-101
  2. Ruta_3_TA-515
  3. Ruta_5_TA-517
  ...
======================================================================

✅ OPTIMIZACIÓN COMPLETADA
```

## 🔍 Verificación de Datos

Para verificar qué datos se están usando del CSV:

```bash
python -c "import pandas as pd; df = pd.read_csv('1_Dataset_Intervenciones_PVD_30062025.csv', sep=';', encoding='latin1', nrows=10); print(df[['CODIGO_RUTA', 'DEPARTAMENTO', 'PROVINCIA']].head())"
```

## 🐛 Solución de Problemas

### Error: "No se pudo cargar el CSV"
- Verifica que el archivo `1_Dataset_Intervenciones_PVD_30062025.csv` esté en la carpeta `Hito-2/`
- Verifica el encoding del archivo

### Error: "No hay datos válidos"
- El sistema intentará generar un dataset de muestra automáticamente
- Verifica que pandas esté instalado: `pip install pandas`

### Error en visualización
- Instala matplotlib: `pip install matplotlib`
- El sistema continuará sin generar la imagen pero creará el JSON

## 📦 Dependencias

```bash
pip install pandas numpy matplotlib scikit-learn geopy openpyxl flask
```

O usa el archivo requirements.txt:
```bash
pip install -r requirements.txt
```

## 🎓 Contexto Académico

Este proyecto es parte del curso de **Complejidad Algorítmica** y demuestra:
- Reducción de complejidad algorítmica
- Uso de clustering para optimización
- Algoritmos exactos vs. heurísticos
- Análisis de escalabilidad

## 📝 Notas

- El sistema genera coordenadas **aproximadas** basadas en departamentos
- Para coordenadas reales, se necesitaría geocoding de cada ubicación
- La optimización es adecuada para demostración y análisis académico
- Para uso en producción, considerar APIs de geocoding reales

## 👥 Autores

Grupo 3 - Complejidad Algorítmica

---

**¿Preguntas?** Consulta los archivos de documentación adicionales:
- `README.md` - Documentación general
- `COMO_EJECUTAR.md` - Guía de ejecución
- `DEPLOY_RENDER.md` - Despliegue en la nube

