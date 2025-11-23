# Hito 2 - Sistema de Optimización de Rutas Avanzado

## Descripción

Este módulo implementa algoritmos avanzados para la optimización de rutas de evacuación, combinando técnicas de **Divide y Vencerás** (clustering con K-Means) y múltiples algoritmos para el **Problema del Viajante (TSP)**.

## Estructura del Proyecto

```
Hito-2/
├── README.md                    # Este archivo
├── requirements.txt             # Dependencias de Python
├── dataset_processor.py         # Módulo de procesamiento y geocodificación
├── kmeans_clustering.py         # Implementación de K-Means (Divide y Vencerás)
├── tsp_algorithms.py           # Algoritmos TSP (Fuerza Bruta, Vecino, Backtracking)
├── sistema_optimizacion.py      # Sistema integrado híbrido
├── main.py                     # Script principal de ejecución
└── dataset_tp_complejidad.xlsx  # Dataset de Provías
```

## Algoritmos Implementados

### 1. **Divide y Vencerás** - K-Means Clustering
- **Archivo**: `kmeans_clustering.py`
- **Complejidad**: O(n × k × i) donde:
  - n = número de puntos
  - k = número de clusters
  - i = iteraciones
- **Propósito**: Divide el problema de N nodos en K sub-problemas de tamaño ≈N/K
- **Ventaja**: Reduce la complejidad factorial O(N!) a O(N²/K)

### 2. **TSP con Fuerza Bruta**
- **Archivo**: `tsp_algorithms.py` - Clase `TSPFuerzaBruta`
- **Complejidad**: O(n!)
- **Uso recomendado**: Clusters pequeños (n ≤ 10)
- **Característica**: Garantiza la solución óptima explorando todas las permutaciones

### 3. **TSP con Vecino más Cercano**
- **Archivo**: `tsp_algorithms.py` - Clase `TSPVecinoMasCercano`
- **Complejidad**: O(n²)
- **Uso recomendado**: Clusters grandes (n > 15)
- **Característica**: Heurística eficiente que proporciona soluciones "suficientemente buenas"

### 4. **TSP con Backtracking**
- **Archivo**: `tsp_algorithms.py` - Clase `TSPBacktracking`
- **Complejidad**: O(n!) con poda
- **Uso recomendado**: Clusters medianos (10 < n ≤ 15)
- **Característica**: Poda ramas no prometedoras para mejorar eficiencia vs Fuerza Bruta

## Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Dependencias principales:
- numpy
- pandas
- scikit-learn
- matplotlib
- geopy
- openpyxl

## Uso

### Ejecución básica

```bash
python main.py
```

### Uso programático

```python
from sistema_optimizacion import OptimizadorRutasHibrido, procesar_dataset_completo

# Opción 1: Usar el procesador completo
resultados = procesar_dataset_completo(
    dataset_path='dataset_tp_complejidad.xlsx',
    n_clusters=5,
    metodo_tsp='auto'
)

# Opción 2: Uso manual paso a paso
import numpy as np

# Cargar coordenadas
coordenadas = np.array([...])  # Array de (lat, lon)
nombres = [...]  # Lista de nombres

# Crear optimizador
optimizador = OptimizadorRutasHibrido(n_clusters=5)

# Ejecutar optimización
resultados = optimizador.optimizar(
    coordenadas, 
    nombres, 
    metodo_tsp='auto'  # 'auto', 'vecino', 'backtracking', 'fuerza_bruta'
)

# Exportar resultados
optimizador.exportar_resultados('resultados.json')

# Visualizar clusters
optimizador.visualizar_resultados(coordenadas, 'clusters.png')
```

## Procesamiento de Dataset

### Con geocodificación real (lento)

```python
from dataset_processor import procesar_dataset_provias

df = procesar_dataset_provias(
    input_path='dataset_tp_complejidad.xlsx',
    output_path='dataset_procesado.xlsx',
    usar_simulacion=False,
    limite_geocoding=100  # Limitar a primeras 100 direcciones
)
```

### Con coordenadas simuladas (rápido para pruebas)

```python
df = procesar_dataset_provias(
    input_path='dataset_tp_complejidad.xlsx',
    output_path='dataset_procesado.xlsx',
    usar_simulacion=True
)
```

## Análisis de Complejidad

### Sistema Completo (Sin Optimización)
- **Complejidad**: O(N!)
- **Problema**: Intratable para N > 15 nodos
- **Ejemplo**: Para N=20, se necesitarían ~2.4×10¹⁸ operaciones

### Sistema Híbrido (Con K-Means + TSP)
- **Complejidad total**: O(n×k×i + K×(N/K)²) ≈ O(n + N²/K)
- **Ventaja**: Reducción drástica de complejidad
- **Ejemplo**: Para N=1000, K=10:
  - Sin optimizar: O(1000!) ≈ ∞ (imposible)
  - Con optimización: O(1000 + 1000²/10) ≈ O(100,000) (factible)

### Comparación por Tamaño de Cluster

| Tamaño (n) | Método Óptimo | Complejidad | Tiempo Estimado |
|------------|---------------|-------------|-----------------|
| n ≤ 10     | Fuerza Bruta  | O(n!)       | < 1 segundo     |
| 10 < n ≤ 15| Backtracking  | O(n!) poda  | < 10 segundos   |
| n > 15     | Vecino        | O(n²)       | < 1 segundo     |

## Resultados Esperados

### Output en consola

```
======================================================================
OPTIMIZACIÓN HÍBRIDA: K-Means + TSP
======================================================================
Total de puntos: 500
Número de clusters: 5
Método TSP: auto

======================================================================
FASE 1: CLUSTERING CON K-MEANS (Divide y Vencerás)
======================================================================
✓ Clustering completado en 0.1234 segundos

Distribución de puntos por cluster:
  Cluster_0: 98 puntos (19.6%)
  Cluster_1: 105 puntos (21.0%)
  ...

======================================================================
FASE 2: OPTIMIZACIÓN INTRA-CLUSTER CON TSP
======================================================================

--- Cluster 0 ---
Puntos en cluster: 98
Método seleccionado: vecino
  ✓ Distancia: 45.32 km
  ✓ Tiempo: 0.0089 segundos
...

======================================================================
RESUMEN DE RESULTADOS
======================================================================
Distancia total combinada: 234.56 km
Tiempo total de ejecución: 2.3456 segundos
Clusters procesados: 5
======================================================================
```

### Archivos generados

1. **resultados_optimizacion.json**: Resultados detallados por cluster
2. **clusters_resultado.png**: Visualización de los clusters formados
3. **dataset_procesado.xlsx**: Dataset con coordenadas geocodificadas

## Validación y Pruebas

### Ejecutar pruebas individuales

```python
# Test de clustering
from kmeans_clustering import ClusteringOptimizer
import numpy as np

coords = np.random.randn(100, 2)
clustering = ClusteringOptimizer(n_clusters=5)
labels = clustering.fit_clusters(coords)
clustering.visualizar_clusters(coords)

# Test de TSP
from tsp_algorithms import comparar_algoritmos

coords_pequeño = np.random.randn(8, 2)
resultados = comparar_algoritmos(coords_pequeño)
```

## Notas Importantes

1. **Geocodificación**: 
   - La geocodificación real es lenta (1-2 segundos por dirección)
   - Usar `usar_simulacion=True` para pruebas rápidas
   - Respetar límites de tasa del servicio de geocodificación

2. **Selección de K (número de clusters)**:
   - Muy pocos clusters: Sub-problemas grandes, algoritmos lentos
   - Muchos clusters: Solución sub-óptima, pérdida de contexto
   - Recomendado: K = √N o K entre 5-10 para datasets típicos

3. **Método TSP**:
   - `'auto'`: El sistema selecciona automáticamente según tamaño
   - Forzar un método solo para análisis comparativo

## Referencias

Este módulo implementa los algoritmos descritos en:
- **Sección 3.2** del documento: Metodología de Optimización
- **Sección 4.2** del documento: Análisis de Algoritmos
- **Divide y Vencerás**: Particionamiento con K-Means
- **TSP**: Fuerza Bruta, Backtracking, y Heurísticas

## Autores

Grupo 03 - Complejidad Algorítmica
Universidad Peruana de Ciencias Aplicadas (UPC)

## Licencia

Este proyecto es parte de un trabajo académico.

