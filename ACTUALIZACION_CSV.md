# ✅ Sistema Actualizado - Usando Base de Datos CSV

## 🎉 Resumen de Cambios

El sistema ahora está **completamente integrado** con la base de datos CSV `1_Dataset_Intervenciones_PVD_30062025.csv`. Ya no es necesario generar archivos Excel manualmente.

## 🚀 Características Implementadas

### 1. ✅ Carga Automática desde CSV
- El sistema lee directamente el archivo CSV de intervenciones viales
- Genera coordenadas automáticamente basadas en departamentos del Perú
- Soporta encoding `latin1` para caracteres especiales

### 2. ✅ Generación Inteligente de Coordenadas
- Usa coordenadas reales de capitales departamentales
- Aplica variación aleatoria para distribuir puntos
- Crea nombres descriptivos: `CODIGO_RUTA_PROVINCIA`

### 3. ✅ Tres Modos de Operación

#### Modo 1: Base de Datos CSV (NUEVO) 🆕
```bash
cd Hito-2
python main.py
```
- Usa automáticamente el CSV si no encuentra Excel
- Procesa hasta 50 puntos por defecto
- Genera rutas reales del Perú

#### Modo 2: Subir Archivo Excel/CSV
- Soporta archivos `.xlsx`, `.xls`, y `.csv`
- Formato: Nombre, Latitud, Longitud
- Límite personalizable de puntos

#### Modo 3: Datos Aleatorios
- Genera datos de muestra para demostración
- Útil para pruebas rápidas

## 📊 Datos del CSV

### Información Disponible
- **Rutas**: TA-101, AR-119, MO-100, etc.
- **Departamentos**: Tacna, Arequipa, Moquegua, Puno, Cusco, etc.
- **Provincias**: 283 provincias únicas
- **Total de registros**: Miles de intervenciones

### Ejemplo de Datos Procesados
```
1. TA-101_JORGE BASADRE
2. TA-103_CANDARAVE
3. AR-119_AREQUIPA
4. MO-100_MARISCAL NIETO
...
```

## 🎯 Cómo Usar el Sistema

### Opción A: Backend Standalone

```bash
cd Hito-2
python main.py
```

**Salida:**
- Archivo JSON con resultados
- Imagen PNG con visualización
- Análisis de complejidad

### Opción B: API Flask (Backend)

```bash
cd Hito-2
python app.py
```

Endpoints:
- `GET /` - Info de la API
- `GET /optimizar` - Ejecuta optimización

### Opción C: Frontend Completo (RECOMENDADO)

```bash
cd Front
python app.py
```

Accede a: `http://localhost:5000`

**Características del Frontend:**
- 🗺️ Mapa interactivo con Leaflet
- 📊 Estadísticas en tiempo real
- 🎨 Visualización de clusters por colores
- 📍 Lista ordenada de puntos a visitar
- 🎛️ Controles configurables

## 🔧 Configuración Avanzada

### En `main.py`:

```python
ARCHIVO_CSV = '1_Dataset_Intervenciones_PVD_30062025.csv'  # Ruta al CSV
MAX_PUNTOS = 50        # Máximo de puntos a procesar
N_CLUSTERS = 5         # Número de clusters
METODO_TSP = 'auto'    # 'auto', 'fuerza_bruta', 'backtracking', 'vecino_cercano'
```

### En `dataset_processor.py`:

```python
def cargar_desde_csv_intervenciones(
    archivo: str = '1_Dataset_Intervenciones_PVD_30062025.csv',
    max_puntos: int = 50
)
```

## 📈 Rendimiento

### Resultados de Pruebas

**Con 15 puntos (3 clusters):**
- ✅ Distancia total: 7.70 km
- ✅ Tiempo de clustering: 1.47s
- ✅ Tiempo de TSP: 10.82s
- ✅ Tiempo total: 12.28s

**Con 25 puntos (5 clusters):**
- ✅ Distancia total: 13.38 km
- ✅ Tiempo de clustering: 1.50s
- ✅ Tiempo de TSP: 1.46s
- ✅ Tiempo total: 2.96s

### Escalabilidad

| Puntos | Clusters | Método TSP | Tiempo Estimado |
|--------|----------|------------|-----------------|
| 10-15  | 2-3      | Fuerza Bruta | < 15s |
| 20-30  | 4-5      | Fuerza Bruta | < 5s |
| 40-50  | 6-8      | Backtracking | < 30s |
| 100+   | 10+      | Vecino Cercano | < 10s |

## 🧪 Pruebas

### Ejecutar Pruebas Automáticas

```bash
cd Front
python test_csv.py
```

**Pruebas incluidas:**
1. ✅ Carga del CSV
2. ✅ Generación de coordenadas
3. ✅ Optimización completa
4. ✅ Exportación de resultados

## 📁 Archivos Generados

### Después de ejecutar `main.py`:

```
Hito-2/
├── resultados_YYYYMMDD_HHMMSS.json   # Resultados completos
├── clusters_YYYYMMDD_HHMMSS.png      # Visualización
└── coordenadas_cache.pkl              # Cache de geocoding
```

### Estructura del JSON:

```json
{
  "ruta_global": [0, 3, 5, 1, ...],
  "distancia_total": 13.38,
  "n_puntos_total": 25,
  "n_clusters": 5,
  "clusters": [...],
  "estadisticas": {
    "tiempo_total": 2.96,
    "tiempo_clustering": 1.50,
    "tiempo_tsp": 1.46
  }
}
```

## 🌍 Departamentos Soportados

El sistema tiene coordenadas predefinidas para los 24 departamentos del Perú:

- **Norte**: Tumbes, Piura, Lambayeque, La Libertad, Cajamarca, Amazonas, Loreto, San Martín
- **Centro**: Ancash, Huánuco, Pasco, Junín, Ucayali, Huancavelica, Lima, ICA
- **Sur**: Ayacucho, Apurímac, Cusco, Puno, Arequipa, Moquegua, Tacna, Madre de Dios

## 🐛 Solución de Problemas

### Error: "CSV no encontrado"
```bash
# Verifica que el archivo existe:
cd Hito-2
dir 1_Dataset_Intervenciones_PVD_30062025.csv
```

### Error: "No se pudieron cargar datos"
- El sistema automáticamente generará datos de muestra
- Revisa el encoding del CSV (debe ser `latin1`)

### Error en Frontend: "Cannot connect"
```bash
# Asegúrate de que Flask está corriendo:
cd Front
python app.py
# Luego accede a http://localhost:5000
```

### Frontend no muestra mapas
- Verifica conexión a internet (usa CDN de Leaflet)
- Revisa la consola del navegador (F12)

## 📦 Dependencias

```bash
pip install pandas numpy matplotlib scikit-learn geopy openpyxl flask
```

O desde `requirements.txt`:
```bash
pip install -r requirements.txt
```

## 📚 Documentación Adicional

- `README.md` - Documentación general del proyecto
- `README_CSV.md` - Guía detallada del uso del CSV
- `COMO_EJECUTAR.md` - Instrucciones de ejecución
- `DEPLOY_RENDER.md` - Despliegue en la nube

## 🎓 Contexto Académico

**Curso:** Complejidad Algorítmica  
**Proyecto:** Sistema de Optimización de Rutas Híbrido  
**Algoritmos:** K-Means + TSP (Fuerza Bruta/Backtracking/Heurístico)

### Objetivos Logrados

✅ Reducción de complejidad algorítmica (O(n!) → O(k × (n/k)!))  
✅ Implementación de clustering para optimización  
✅ Comparación de algoritmos exactos vs. heurísticos  
✅ Análisis de escalabilidad  
✅ Integración con datos reales  

## 👥 Autores

**Grupo 3** - Complejidad Algorítmica

---

## 🎯 Próximos Pasos

1. ✅ ~~Integrar base de datos CSV~~
2. ✅ ~~Actualizar frontend con modo CSV~~
3. ✅ ~~Crear pruebas automatizadas~~
4. 🔜 Agregar más métricas de análisis
5. 🔜 Implementar visualización 3D
6. 🔜 Exportar a formatos adicionales (KML, GeoJSON)

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:
1. Revisa esta documentación
2. Ejecuta las pruebas automatizadas
3. Consulta los archivos README adicionales
4. Verifica los logs de ejecución

---

**Última actualización:** 23 de Noviembre, 2024  
**Versión:** 2.0 - Integración CSV completa

