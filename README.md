# RutaFix - Sistema de Optimización de Rutas para Técnicos en Lima

**Proyecto de Complejidad Algorítmica - Grupo 03**  
Universidad Peruana de Ciencias Aplicadas (UPC) - 2024-2

---

## Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación](#instalación)
4. [Cómo Usar la Aplicación](#cómo-usar-la-aplicación)
5. [Guía Detallada por Funcionalidad](#guía-detallada-por-funcionalidad)
6. [Algoritmos Implementados](#algoritmos-implementados)
7. [Estructura del Proyecto](#estructura-del-proyecto)

---

## Descripción del Proyecto

RutaFix es un sistema web que optimiza rutas para equipos técnicos que realizan intervenciones domiciliarias y mantenimiento en Lima Metropolitana.

### El Problema

Las empresas de servicios enfrentan:
- Tiempos muertos entre visitas
- Recorridos redundantes
- Distribución desbalanceada de trabajo
- Alto consumo de combustible

### La Solución

Sistema que combina tres algoritmos:
- **K-Means Clustering**: Agrupa puntos en zonas manejables
- **TSP (Traveling Salesman Problem)**: Optimiza el orden de visitas
- **Dijkstra**: Calcula la ruta más corta entre dos puntos

---

## Requisitos Previos

Antes de comenzar, necesitas tener instalado:

- **Python 3.8 o superior**
  - Verifica con: `python --version`
  - Descarga desde: https://www.python.org/downloads/

- **pip** (incluido con Python)
  - Verifica con: `pip --version`

- **Navegador web** (Chrome, Firefox, Edge, etc.)

---

## Instalación

### Paso 1: Abrir Terminal/Consola

**En Windows:**
- Presiona `Win + R`
- Escribe `powershell` y presiona Enter

**En Mac/Linux:**
- Busca "Terminal" en aplicaciones

### Paso 2: Navegar a la Carpeta del Proyecto

```bash
cd C:\Users\Jafeth\IdeaProjects\FinalProyect_ComplejidadAlgo-Grupo3\Front
```

> **Nota:** Ajusta la ruta según donde tengas el proyecto

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Esto instalará:**
- Flask (servidor web)
- Folium (mapas interactivos)
- NumPy (cálculos numéricos)
- Scikit-learn (K-Means)
- Geopy (distancias geográficas)
- Y otras librerías necesarias

**Tiempo estimado:** 2-3 minutos

---

## Cómo Usar la Aplicación

### Paso 1: Iniciar el Servidor

En la terminal, dentro de la carpeta `Front`, ejecuta:

```bash
python app.py
```

Verás un mensaje como:

```
======================================================================
🚀 Sistema de Optimización de Rutas API
======================================================================
📍 Puerto: 5000
🔧 Modo: development
✓ API disponible en: http://localhost:5000
======================================================================
```

### Paso 2: Abrir en el Navegador

**Opción A - Automático:**
- El navegador debería abrirse automáticamente

**Opción B - Manual:**
1. Abre tu navegador
2. Escribe en la barra de direcciones: `http://localhost:5000`
3. Presiona Enter

### Paso 3: Explorar la Aplicación

Verás la interfaz de RutaFix con 3 pestañas:
1. **Optimización de Rutas** - Principal
2. **Ruta Dijkstra A→B** - Ruta más corta
3. **Información** - Detalles técnicos

---

## Guía Detallada por Funcionalidad

### 🎯 Funcionalidad 1: Optimización de Rutas

**¿Qué hace?**
Toma múltiples puntos de visita, los agrupa en zonas (clusters) y calcula la ruta óptima para cada zona.

#### Paso a Paso:

**1. Cargar Puntos de Ejemplo**
   - Click en el botón **"Cargar Ejemplo Lima"**
   - Se cargarán 8 puntos automáticamente (Miraflores, San Isidro, etc.)

**2. Configurar Parámetros**

   a. **Número de Clusters:**
   - Representa cuántas zonas o técnicos tienes
   - Valor recomendado: 2-5
   - Ejemplo: Si tienes 3 técnicos, usa 3 clusters

   b. **Método TSP:**
   - **Automático (Recomendado):** El sistema elige el mejor método
   - **Fuerza Bruta:** Óptimo pero solo para ≤10 puntos por cluster
   - **Backtracking:** Óptimo para ≤15 puntos
   - **Vecino más Cercano:** Rápido para muchos puntos

**3. Ejecutar Optimización**
   - Click en **"Optimizar Rutas"**
   - Espera unos segundos (aparecerá un indicador de carga)

**4. Ver Resultados**

   El mapa mostrará:
   - **Puntos de colores:** Cada color = un cluster diferente
   - **Líneas:** Conectan los puntos en el orden óptimo
   - **Estrella verde:** Punto de inicio
   - **Panel superior derecho:** Estadísticas

   Estadísticas que verás:
   - **Clusters:** Número de zonas creadas
   - **km Totales:** Distancia total optimizada
   - **Tiempo Cálculo:** Tiempo que tomó optimizar
   - **Método TSP:** Algoritmo usado

#### Agregar Puntos Manualmente:

**1. Click en "+ Agregar Punto"**

**2. Llenar el formulario:**
   - **Nombre:** Ej. "Casa del Sr. García"
   - **Latitud:** Ej. -12.0464
   - **Longitud:** Ej. -77.0428

**3. Repetir para cada punto**

**4. Click en "Optimizar Rutas"**

> **Tip:** Puedes usar Google Maps para obtener coordenadas:
> - Busca un lugar en Google Maps
> - Click derecho sobre el punto
> - Las coordenadas aparecen en el menú

---

### 🗺️ Funcionalidad 2: Ruta Dijkstra A→B

**¿Qué hace?**
Calcula la ruta más corta entre dos puntos específicos usando el algoritmo de Dijkstra.

#### Paso a Paso:

**1. Ir a la pestaña "Ruta Dijkstra A→B"**
   - Click en la segunda pestaña

**2. Cargar Ejemplo (Opcional)**
   - Click en "Cargar Ejemplo"
   - Se cargarán Miraflores → San Isidro

**3. Ingresar Punto de Inicio (A)**
   - **Nombre:** Ej. "Oficina Central"
   - **Latitud:** Ej. -12.0565
   - **Longitud:** Ej. -77.0538

**4. Ingresar Punto de Destino (B)**
   - **Nombre:** Ej. "Cliente VIP"
   - **Latitud:** Ej. -12.0697
   - **Longitud:** Ej. -77.0381

**5. Calcular Ruta**
   - Click en "Calcular Ruta"

**6. Ver Resultados**
   - **Línea azul oscura:** Ruta más corta
   - **Marcador verde:** Punto de inicio
   - **Marcador rojo:** Punto de destino
   - **Panel superior derecho:** Estadísticas

   Estadísticas:
   - **km:** Distancia total
   - **Nodos Visitados:** Puntos intermedios
   - **Tiempo Cálculo:** Velocidad del algoritmo

---

### ℹ️ Funcionalidad 3: Información

**¿Qué contiene?**
- Descripción de algoritmos
- Análisis de complejidad
- Tabla comparativa de rendimiento

**Para qué sirve:**
- Entender cómo funciona el sistema
- Ver comparativas técnicas
- Información del proyecto

---

## Algoritmos Implementados

### 1. K-Means Clustering (Divide y Vencerás)

**Complejidad:** O(n × k × i)

**¿Qué hace?**
Agrupa N puntos en K clusters (zonas) minimizando la distancia intra-cluster.

**Ventaja:**
Convierte un problema de N! en K problemas de (N/K)! cada uno.

**Ejemplo:**
- 20 puntos sin agrupar: 2.4 × 10¹⁸ operaciones
- 20 puntos en 5 clusters: ~120 operaciones

---

### 2. TSP - Fuerza Bruta

**Complejidad:** O(n!)

**¿Qué hace?**
Prueba todas las permutaciones posibles de rutas y elige la más corta.

**Cuándo usarlo:**
Solo para n ≤ 10 puntos

**Ventaja:**
Garantiza la solución óptima

---

### 3. TSP - Backtracking con Poda

**Complejidad:** O(n!) pero optimizado

**¿Qué hace?**
Explora rutas pero descarta ramas que no pueden ser óptimas.

**Cuándo usarlo:**
Para n ≤ 15 puntos

**Ventaja:**
10-100x más rápido que fuerza bruta

---

### 4. TSP - Vecino más Cercano

**Complejidad:** O(n²)

**¿Qué hace?**
Heurística greedy: siempre va al punto más cercano no visitado.

**Cuándo usarlo:**
Para n > 15 puntos

**Ventaja:**
Muy rápido, escalable a miles de puntos

---

### 5. Dijkstra

**Complejidad:** O(E log V)

**¿Qué hace?**
Encuentra el camino más corto entre dos nodos en un grafo ponderado.

**Ventaja:**
Garantiza el camino óptimo entre dos puntos

---

## Estructura del Proyecto

```
FinalProyect_ComplejidadAlgo-Grupo3/
│
├── Front/                          # Aplicación web principal
│   ├── app.py                    # Servidor Flask
│   ├── templates/                # Interfaz web
│   │   └── index.html           # Página principal
│   ├── routes/                   # Endpoints
│   │   ├── web.py               # Rutas de la web
│   │   ├── optimization.py      # API optimización
│   │   └── dijkstra_service.py  # Servicio Dijkstra
│   ├── services/                 # Lógica de negocio
│   │   ├── tsp_service.py       # Algoritmos TSP
│   │   ├── clustering_service.py # K-Means
│   │   └── dijkstra_service.py  # Dijkstra
│   └── requirements.txt          # Dependencias
│
├── Hito-2/                       # Scripts Python standalone
│   ├── main.py                   # Script de prueba
│   ├── kmeans_clustering.py      # K-Means
│   └── tsp_algorithms.py         # TSP
│
└── README.md                     # Este archivo
```

---

## Solución de Problemas Comunes

### Problema: "ModuleNotFoundError"

**Solución:**
```bash
cd Front
pip install -r requirements.txt
```

### Problema: "Puerto 5000 en uso"

**Solución Windows:**
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

**Solución Mac/Linux:**
```bash
lsof -ti:5000 | xargs kill -9
```

### Problema: La página no carga

**Solución:**
1. Verifica que el servidor esté corriendo (no cierres la terminal)
2. Intenta: `http://127.0.0.1:5000` en lugar de `localhost`
3. Prueba otro navegador

### Problema: "pip no se reconoce"

**Solución:**
- Reinstala Python marcando "Add to PATH"
- O usa: `python -m pip install -r requirements.txt`

---

## Pruebas del Sistema

### Probar la API REST:

```bash
cd Front
python test_api.py
```

**Resultado esperado:** 7/7 tests pasando

---

## Tecnologías Utilizadas

- **Python 3.13** - Lenguaje principal
- **Flask** - Framework web
- **Folium** - Mapas interactivos
- **NumPy** - Cálculos numéricos
- **Scikit-learn** - K-Means clustering
- **Geopy** - Geocodificación y distancias geodésicas

---

## Documentación Técnica

Ver `TF-Complejidad-Grupo03.md` para el documento técnico completo.

---

## Autores

**Grupo 03 - Complejidad Algorítmica**
Universidad Peruana de Ciencias Aplicadas (UPC)
Ciclo 2024-2

---

## Soporte

Para problemas o preguntas:
1. Revisa la sección "Solución de Problemas"
2. Verifica que todas las dependencias estén instaladas
3. Consulta el documento técnico

---

**La aplicación está lista para usar. Ejecuta `python app.py` en la carpeta `Front` y accede a http://localhost:5000**


**Proyecto de Complejidad Algorítmica - Grupo 03**
Universidad Peruana de Ciencias Aplicadas (UPC) - 2024-2

## 📋 Descripción

RutaFix es un sistema de optimización de rutas para equipos técnicos que realizan intervenciones domiciliarias y de mantenimiento en Lima Metropolitana. Utiliza algoritmos avanzados de grafos y clustering para minimizar tiempos de traslado, consumo de combustible y mejorar la eficiencia operativa.

### Problema

La planificación manual de rutas genera:
- ⏰ Tiempos muertos excesivos entre visitas
- 🔄 Recorridos redundantes
- ⚖️ Distribución desequilibrada de carga de trabajo
- 💰 Alto consumo de combustible y costos operativos

### Solución

Sistema híbrido que combina:
1. **K-Means Clustering** (Divide y Vencerás) - Agrupa puntos en zonas
2. **TSP** (Fuerza Bruta/Backtracking/Vecino más Cercano) - Optimiza rutas por zona
3. **Dijkstra** - Calcula caminos mínimos entre puntos específicos

## 🎯 Características

### Aplicación Web Interactiva
- 🗺️ Visualización de rutas en mapas interactivos (Folium)
- 📍 Optimización de múltiples puntos con clustering
- 🧭 Cálculo de ruta más corta A→B con Dijkstra
- 📊 Estadísticas en tiempo real
- 🎨 Interfaz moderna y responsive

### Algoritmos Implementados

| Algoritmo | Complejidad | Uso |
|-----------|-------------|-----|
| **K-Means** | O(n×k×i) | Clustering (Divide y Vencerás) |
| **TSP Fuerza Bruta** | O(n!) | Óptimo para n≤10 |
| **TSP Backtracking** | O(n!) con poda | Óptimo para n≤15 |
| **TSP Vecino más Cercano** | O(n²) | Heurística escalable |
| **Dijkstra** | O(E log V) | Camino más corto A→B |

### Reducción de Complejidad

| N Puntos | Sin Optimizar | Con K-Means+TSP | Mejora |
|----------|---------------|-----------------|--------|
| 10 | ~3.6M ops | ~100 ops | 36,000x |
| 50 | INTRATABLE | ~2,500 ops | ∞ |
| 1000 | IMPOSIBLE | ~100,000 ops | ∞ |

## 🚀 Instalación y Ejecución

### Opción 1: Aplicación Web (RECOMENDADO)

```bash
# 1. Instalar dependencias
cd Front
pip install -r requirements.txt

# 2. Ejecutar servidor
python app.py
```

**La aplicación se abrirá automáticamente en:** `http://localhost:5000`

### Opción 2: Scripts Python (Hito-2)

```bash
cd Hito-2
pip install -r requirements.txt
python main.py
```

## 📱 Uso de la Aplicación Web

### 1. Optimización de Rutas
1. Ingresa los puntos de visita (nombre, latitud, longitud)
2. Configura número de clusters (técnicos/zonas)
3. Selecciona método TSP
4. Click en "Optimizar Rutas"
5. Visualiza el mapa con clusters y rutas optimizadas

### 2. Ruta Dijkstra A→B
1. Ingresa punto de inicio (A)
2. Ingresa punto de destino (B)
3. Click en "Calcular Ruta"
4. Visualiza la ruta más corta en el mapa

## 📊 API REST

También disponible como API REST:

```bash
# Optimizar rutas
POST /api/optimize
{
  "coordenadas": [...],
  "n_clusters": 3,
  "metodo_tsp": "auto"
}

# Info de algoritmos
GET /api/algorithms/info

# Análisis de complejidad
GET /api/algorithms/complexity
```

## 📁 Estructura del Proyecto

```
FinalProyect_ComplejidadAlgo-Grupo3/
├── Front/                          # Backend Flask + Web App
│   ├── app.py                    # Aplicación principal
│   ├── templates/                # HTML de la web app
│   │   └── index.html           # Interfaz RutaFix
│   ├── routes/                   # Endpoints
│   │   ├── web.py               # Rutas web app
│   │   ├── optimization.py      # API optimización
│   │   ├── algorithms.py        # Info algoritmos
│   │   └── dataset.py           # Datasets
│   ├── services/                 # Lógica de negocio
│   │   ├── tsp_service.py       # Servicio TSP
│   │   ├── clustering_service.py # Servicio clustering
│   │   └── dijkstra_service.py  # Servicio Dijkstra
│   └── utils/                    # Utilidades
│
├── Hito-2/                       # Scripts Python standalone
│   ├── main.py                   # Script principal
│   ├── kmeans_clustering.py      # K-Means
│   ├── tsp_algorithms.py         # TSP
│   └── sistema_optimizacion.py   # Sistema híbrido
│
└── README.md                     # Este archivo
```

## 🧪 Pruebas

```bash
# Probar API
cd Front
python test_api.py

# Resultado esperado: 7/7 tests pasando
```

## 🛠️ Tecnologías

- **Python 3.13**
- **Flask** - Framework web
- **Folium** - Mapas interactivos
- **NumPy** - Cálculos numéricos
- **Scikit-learn** - K-Means clustering
- **Geopy** - Geocodificación y distancias

## 📖 Documentación

Ver `TF-Complejidad-Grupo03.md` para el documento técnico completo del proyecto.

## 👥 Autores

**Grupo 03 - Complejidad Algorítmica**
- Universidad Peruana de Ciencias Aplicadas (UPC)
- Ciclo: 2024-2

## 🎓 Contexto Académico

Proyecto final del curso de Complejidad Algorítmica enfocado en la aplicación práctica de:
- Divide y Vencerás (K-Means)
- Fuerza Bruta (TSP)
- Backtracking con Poda
- Heurísticas (Vecino más Cercano)
- Algoritmos de Grafos (Dijkstra)

---

**🚀 ¡La aplicación web está lista para usar! Ejecuta `python app.py` en la carpeta `Front` y accede a http://localhost:5000**


## 📁 Estructura del Proyecto

```
FinalProyect_ComplejidadAlgo-Grupo3/
│
├── Hito-2/                    # ✅ Algoritmos avanzados (K-Means + TSP)
│   ├── kmeans_clustering.py         # Clustering Divide y Vencerás
│   ├── tsp_algorithms.py            # 3 Algoritmos TSP
│   ├── sistema_optimizacion.py     # Sistema híbrido integrado
│   ├── dataset_processor.py         # Procesamiento de datasets
│   ├── main.py                      # Script principal ejecutable
│   └── requirements.txt
│
├── Front/                      # ✅ Backend Flask API REST
│   ├── app.py                       # Aplicación principal
│   ├── config.py                    # Configuración
│   ├── routes/                      # Endpoints API
│   ├── services/                    # Lógica de negocio
│   ├── utils/                       # Utilidades
│   ├── test_api.py                  # Suite de pruebas
│   └── requirements.txt
│
├── sore/                      # Frontend Next.js (referencia)
├── Hito-1/                    # Implementación básica (referencia)
└── README.md                  # Este archivo
```

## 🎯 Características Principales

### Algoritmos Implementados

#### **K-Means Clustering** (Divide y Vencerás)
- ✅ Complejidad: O(n × k × i)
- ✅ Divide N puntos en K clusters manejables
- ✅ Reduce O(N!) a O(N²/K)

#### **TSP - Fuerza Bruta**
- ✅ Complejidad: O(n!)
- ✅ Solución óptima garantizada
- ✅ Viable para n ≤ 10

#### **TSP - Backtracking con Poda**
- ✅ Complejidad: O(n!) con optimización
- ✅ 10-100x más rápido que Fuerza Bruta
- ✅ Viable para n ≤ 15

#### **TSP - Vecino más Cercano**
- ✅ Complejidad: O(n²)
- ✅ Heurística eficiente
- ✅ Escalable a miles de nodos

### Sistema Híbrido
- 🔹 Combina K-Means con TSP
- 🔹 Escalable hasta 10,000+ puntos
- 🔹 Balance entre optimalidad y eficiencia

## 🚀 Instalación y Ejecución

### Prerequisitos
- Python 3.8+
- pip

### Opción 1: Ejecutar Hito-2 (Standalone)

```bash
# Ir a la carpeta Hito-2
cd Hito-2

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el sistema
python main.py
```

**Resultado:**
- Genera archivos `resultados_*.json` con las rutas optimizadas
- Crea visualizaciones `clusters_*.png` de los clusters y rutas

### Opción 2: Ejecutar Backend API

```bash
# Ir a la carpeta back
cd Front

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python app.py
```

**Servidor disponible en:** `http://localhost:5000`

**Probar la API:**
```bash
# En otra terminal
cd Front
python test_api.py
```

## 📚 Uso de la API

### Endpoints Disponibles

#### 1. Health Check
```bash
GET http://localhost:5000/api/health
```

#### 2. Optimización Completa
```bash
POST http://localhost:5000/api/optimize
Content-Type: application/json

{
  "coordenadas": [
    {"lat": -12.0464, "lon": -77.0428, "nombre": "Lima"},
    {"lat": -12.0565, "lon": -77.0538, "nombre": "Miraflores"}
  ],
  "n_clusters": 2,
  "metodo_tsp": "auto"
}
```

#### 3. Información de Algoritmos
```bash
GET http://localhost:5000/api/algorithms/info
```

#### 4. Análisis de Complejidad
```bash
GET http://localhost:5000/api/algorithms/complexity
```

#### 5. Recomendaciones
```bash
GET http://localhost:5000/api/algorithms/recommendations
```

#### 6. Dataset de Muestra
```bash
GET http://localhost:5000/api/dataset/sample
```

## 🧪 Pruebas

### Backend
```bash
cd Front
python test_api.py
```

**Resultado esperado:** ✅ 7/7 pruebas exitosas

## 📊 Análisis de Complejidad

### Sin Optimización
- **Problema:** TSP sobre N puntos
- **Complejidad:** O(N!)
- **Límite práctico:** N ≤ 15

### Con Sistema Híbrido
- **Estrategia:** K-Means + TSP por cluster
- **Complejidad:** O(N + N²/K)
- **Escalable hasta:** N > 10,000

### Comparación

| N Puntos | Sin Optimizar | Con Híbrido (K=10) | Reducción |
|----------|---------------|-------------------|-----------|
| 10       | ~3.6M ops     | ~100 ops          | 36,000x   |
| 50       | Intratable    | ~2,500 ops        | ∞         |
| 100      | Imposible     | ~10,000 ops       | ∞         |
| 1000     | Imposible     | ~100,000 ops      | ∞         |

## 📈 Ejemplo de Ejecución

### Hito-2 Standalone
```
🚀 SISTEMA DE OPTIMIZACIÓN DE RUTAS DE EVACUACIÓN
✓ Dataset generado: 20 puntos
✓ Clusters creados: 5
✓ TSP resuelto para cada cluster
📊 RESUMEN:
  - Puntos totales: 20
  - Clusters: 5
  - Distancia total: 6.0555
  - Tiempo total: 1.69s
✅ OPTIMIZACIÓN COMPLETADA
```

### Backend API
```
🧪 SUITE DE PRUEBAS
✓ PASS - Health Check
✓ PASS - Info de Algoritmos
✓ PASS - Análisis de Complejidad
✓ PASS - Recomendaciones
✓ PASS - Dataset de Muestra
✓ PASS - Optimización Básica
✓ PASS - Validación de Errores
🎉 ¡Todas las pruebas pasaron!
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.13**
- **NumPy** - Operaciones matemáticas
- **Pandas** - Procesamiento de datos
- **Scikit-learn** - Clustering K-Means
- **Flask** - API REST
- **Matplotlib** - Visualizaciones
- **Geopy** - Cálculos geográficos

## 📖 Documentación Adicional

- `GUIA_COMPLETA.md` - Guía detallada del proyecto
- `INICIO_RAPIDO.md` - Instrucciones de inicio rápido
- `PROYECTO_COMPLETADO.md` - Resumen ejecutivo
- `Hito-2/README.md` - Detalles de algoritmos
- `Front/README.md` - Documentación de API

## ✅ Estado del Proyecto

- ✅ Hito-2: Implementado y funcionando
- ✅ Backend API: Implementado y probado (7/7 tests pasando)
- ✅ Documentación: Completa
- ✅ Pruebas: Todas exitosas

## 👥 Autores

**Grupo 03 - Complejidad Algorítmica**
- Universidad Peruana de Ciencias Aplicadas (UPC)
- Ciclo: 2024-2

## 🎓 Contexto Académico

Proyecto final del curso de Complejidad Algorítmica enfocado en la optimización de rutas de evacuación usando técnicas avanzadas de grafos y clustering.

---

**🎉 Proyecto completado y funcional - Listo para usar!**


