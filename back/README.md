# Backend API - Sistema de Optimización de Rutas

## Descripción

API REST backend para el sistema de optimización de rutas de evacuación. Provee endpoints para procesar datasets, ejecutar algoritmos de optimización y obtener resultados.

## Tecnologías

- **Framework**: Flask (Python)
- **CORS**: Flask-CORS
- **Procesamiento**: NumPy, Pandas, Scikit-learn
- **Algoritmos**: Implementaciones personalizadas de TSP y K-Means

## Estructura

```
back/
├── README.md                 # Este archivo
├── requirements.txt          # Dependencias
├── app.py                   # Aplicación Flask principal
├── config.py                # Configuración
├── routes/
│   ├── __init__.py
│   ├── optimization.py      # Rutas de optimización
│   ├── dataset.py           # Rutas de dataset
│   └── algorithms.py        # Rutas de algoritmos individuales
├── services/
│   ├── __init__.py
│   ├── clustering_service.py   # Servicio de clustering
│   ├── tsp_service.py          # Servicio TSP
│   └── dataset_service.py      # Servicio de dataset
├── utils/
│   ├── __init__.py
│   ├── validators.py        # Validadores
│   └── responses.py         # Formateadores de respuesta
└── uploads/                 # Carpeta para archivos subidos
```

## Instalación

### 1. Crear entorno virtual (recomendado)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecución

### Modo desarrollo

```bash
python app.py
```

El servidor estará disponible en: `http://localhost:5000`

### Modo producción

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Endpoints

### 1. Health Check

```http
GET /api/health
```

**Response:**
```json
{
  "status": "ok",
  "message": "Sistema de Optimización de Rutas API",
  "version": "1.0.0"
}
```

### 2. Optimización Completa

```http
POST /api/optimize
Content-Type: application/json
```

**Request Body:**
```json
{
  "coordenadas": [
    {"lat": -12.0464, "lon": -77.0428, "nombre": "Punto 1"},
    {"lat": -12.0565, "lon": -77.0538, "nombre": "Punto 2"}
  ],
  "n_clusters": 5,
  "metodo_tsp": "auto"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "clusters": {
      "0": {
        "ruta": ["Punto 1", "Punto 3", "Punto 1"],
        "distancia": 12.5,
        "tiempo": 0.002,
        "metodo": "vecino",
        "n_puntos": 10
      }
    },
    "distancia_total": 65.3,
    "tiempo_total": 0.05,
    "n_clusters": 5
  }
}
```

### 3. Solo Clustering

```http
POST /api/clustering
Content-Type: application/json
```

**Request Body:**
```json
{
  "coordenadas": [
    {"lat": -12.0464, "lon": -77.0428},
    {"lat": -12.0565, "lon": -77.0538}
  ],
  "n_clusters": 5
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "labels": [0, 1, 0, 2, 1],
    "centroides": [
      {"lat": -12.0464, "lon": -77.0428},
      {"lat": -12.0565, "lon": -77.0538}
    ],
    "estadisticas": {
      "Cluster_0": {
        "num_puntos": 50,
        "porcentaje": 25.0
      }
    }
  }
}
```

### 4. TSP Individual

```http
POST /api/tsp
Content-Type: application/json
```

**Request Body:**
```json
{
  "coordenadas": [
    {"lat": -12.0464, "lon": -77.0428, "nombre": "A"},
    {"lat": -12.0565, "lon": -77.0538, "nombre": "B"}
  ],
  "metodo": "vecino",
  "inicio": 0
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "ruta": ["A", "B", "C", "A"],
    "distancia": 15.3,
    "tiempo": 0.001,
    "metodo": "vecino"
  }
}
```

### 5. Comparar Algoritmos TSP

```http
POST /api/tsp/compare
Content-Type: application/json
```

**Request Body:**
```json
{
  "coordenadas": [
    {"lat": -12.0464, "lon": -77.0428, "nombre": "A"},
    {"lat": -12.0565, "lon": -77.0538, "nombre": "B"}
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "Vecino más Cercano": {
      "ruta": ["A", "B", "A"],
      "distancia": 15.3,
      "tiempo": 0.001
    },
    "Backtracking": {
      "ruta": ["A", "B", "A"],
      "distancia": 15.3,
      "tiempo": 0.005,
      "nodos_explorados": 12
    }
  }
}
```

### 6. Procesar Dataset

```http
POST /api/dataset/process
Content-Type: multipart/form-data
```

**Form Data:**
- `file`: Archivo Excel (.xlsx)
- `usar_simulacion`: true/false (opcional, default: true)
- `limite_geocoding`: número (opcional)

**Response:**
```json
{
  "status": "success",
  "data": {
    "num_puntos": 100,
    "coordenadas": [...],
    "nombres": [...]
  },
  "message": "Dataset procesado exitosamente"
}
```

### 7. Obtener Información de Algoritmos

```http
GET /api/algorithms/info
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "kmeans": {
      "nombre": "K-Means Clustering",
      "complejidad": "O(n*k*i)",
      "descripcion": "Divide y Vencerás...",
      "uso": "Particionamiento del problema"
    },
    "fuerza_bruta": {
      "nombre": "TSP Fuerza Bruta",
      "complejidad": "O(n!)",
      "descripcion": "Solución óptima...",
      "uso": "Clusters pequeños (n≤10)"
    }
  }
}
```

## Manejo de Errores

Todos los endpoints devuelven errores en el siguiente formato:

```json
{
  "status": "error",
  "message": "Descripción del error",
  "code": "ERROR_CODE"
}
```

### Códigos de Error Comunes

- `400`: Bad Request - Datos de entrada inválidos
- `404`: Not Found - Recurso no encontrado
- `500`: Internal Server Error - Error del servidor
- `413`: Payload Too Large - Archivo muy grande

## Configuración

### Variables de Entorno

Crear archivo `.env`:

```env
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=tu_clave_secreta_aqui
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads
ALLOWED_EXTENSIONS=xlsx,xls,csv
```

### Configuración de CORS

Por defecto, el backend acepta peticiones desde:
- `http://localhost:3000` (Next.js frontend)
- `http://localhost:3001`

Modificar en `app.py` si es necesario.

## Pruebas

### Con cURL

```bash
# Health check
curl http://localhost:5000/api/health

# Optimización
curl -X POST http://localhost:5000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "coordenadas": [
      {"lat": -12.0464, "lon": -77.0428, "nombre": "A"},
      {"lat": -12.0565, "lon": -77.0538, "nombre": "B"}
    ],
    "n_clusters": 2,
    "metodo_tsp": "auto"
  }'
```

### Con Python requests

```python
import requests

# Health check
response = requests.get('http://localhost:5000/api/health')
print(response.json())

# Optimización
data = {
    'coordenadas': [
        {'lat': -12.0464, 'lon': -77.0428, 'nombre': 'A'},
        {'lat': -12.0565, 'lon': -77.0538, 'nombre': 'B'}
    ],
    'n_clusters': 2,
    'metodo_tsp': 'auto'
}
response = requests.post('http://localhost:5000/api/optimize', json=data)
print(response.json())
```

## Seguridad

### Recomendaciones para Producción

1. **Variables de entorno**: No hardcodear claves
2. **Rate limiting**: Implementar límites de peticiones
3. **Validación**: Validar todos los inputs
4. **HTTPS**: Usar certificados SSL
5. **Autenticación**: Implementar JWT o similar si es necesario

## Despliegue

### Docker (Recomendado)

Ver `Dockerfile` incluido en el proyecto.

```bash
docker build -t rutafix-api .
docker run -p 5000:5000 rutafix-api
```

### Heroku

```bash
heroku create rutafix-api
git push heroku main
```

## Logs

Los logs se guardan en:
- Consola en modo desarrollo
- Archivo `app.log` en modo producción

## Licencia

Proyecto académico - UPC

