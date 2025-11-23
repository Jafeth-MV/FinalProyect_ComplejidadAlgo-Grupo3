# 🚀 Sistema de Optimización de Rutas de Evacuación

Sistema completo para optimización de rutas de evacuación usando algoritmos avanzados de grafos y machine learning.

## 📁 Estructura del Proyecto

```
Sistema-de-optimizacion-de-rutas-de-evacuacion/
│
├── Hito-1/                    # Implementación básica con Dijkstra
│   ├── dataset.py
│   ├── dijkstra.py
│   ├── nodos_aristas.py
│   └── dataset_tp_complejidad.xlsx
│
├── Hito-2/                    # Algoritmos avanzados (K-Means + TSP)
│   ├── kmeans_clustering.py         # Divide y Vencerás
│   ├── tsp_algorithms.py            # Fuerza Bruta, Backtracking, Vecino
│   ├── sistema_optimizacion.py     # Sistema híbrido integrado
│   ├── dataset_processor.py         # Procesamiento de datasets
│   ├── main.py                      # Script principal
│   ├── requirements.txt
│   └── README.md
│
├── sore/                      # Frontend Next.js
│   ├── app/
│   │   ├── page.tsx                 # Página principal
│   │   ├── components/              # Componentes React
│   │   ├── api/                     # API Routes
│   │   └── lib/                     # Utilidades y datos
│   ├── package.json
│   └── README.md
│
├── back/                      # Backend Flask API
│   ├── app.py                       # Aplicación principal
│   ├── config.py                    # Configuración
│   ├── routes/                      # Endpoints
│   │   ├── optimization.py
│   │   ├── dataset.py
│   │   └── algorithms.py
│   ├── services/                    # Lógica de negocio
│   │   ├── clustering_service.py
│   │   └── tsp_service.py
│   ├── utils/                       # Utilidades
│   ├── test_api.py                  # Suite de pruebas
│   ├── requirements.txt
│   └── README.md
│
├── TF-Complejidad-Grupo03.md  # Documento del proyecto
└── README.md                  # Este archivo
```

## 🎯 Características Principales

### Algoritmos Implementados

#### 1. **Hito 1 - Dijkstra** (Algoritmo de Camino Más Corto)
- ✅ Complejidad: O(E log V)
- ✅ Uso: Rutas específicas punto a punto
- ✅ Implementación con heap priority queue

#### 2. **Hito 2 - Sistema Híbrido Avanzado**

**Divide y Vencerás - K-Means Clustering**
- ✅ Complejidad: O(n × k × i)
- ✅ Divide N puntos en K clusters manejables
- ✅ Reduce O(N!) a O(N²/K)

**TSP - Fuerza Bruta**
- ✅ Complejidad: O(n!)
- ✅ Solución óptima garantizada
- ✅ Viable para n ≤ 10

**TSP - Backtracking con Poda**
- ✅ Complejidad: O(n!) con optimización
- ✅ 10-100x más rápido que Fuerza Bruta
- ✅ Viable para n ≤ 15

**TSP - Vecino más Cercano**
- ✅ Complejidad: O(n²)
- ✅ Heurística eficiente
- ✅ Escalable a miles de nodos

### Frontend (Next.js + React)
- 🎨 Interfaz moderna y responsiva
- 📊 Visualización interactiva de grafos
- 🗺️ Integración con D3.js y vis-network
- ⚡ Server-side rendering

### Backend (Flask API)
- 🔌 API REST completa
- 📡 CORS configurado
- 🔍 Validación de datos
- 📝 Documentación integrada

## 🚀 Instalación y Ejecución

### Prerequisitos

- Python 3.8+
- Node.js 16+
- npm o yarn

### Opción 1: Instalación Rápida (Script Automatizado)

#### Windows PowerShell:
```powershell
# Ejecutar desde la raíz del proyecto
.\install.ps1
```

#### Linux/Mac:
```bash
chmod +x install.sh
./install.sh
```

### Opción 2: Instalación Manual

#### 1. Backend (Flask)

```bash
cd back

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar configuración
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Ejecutar servidor
python app.py
```

El backend estará disponible en: `http://localhost:5000`

#### 2. Frontend (Next.js)

```bash
cd sore

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```

El frontend estará disponible en: `http://localhost:3000`

#### 3. Hito-2 (Scripts Python)

```bash
cd Hito-2

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar sistema de optimización
python main.py
```

## 📖 Uso

### Backend API

#### 1. Health Check
```bash
curl http://localhost:5000/api/health
```

#### 2. Optimización Completa
```bash
curl -X POST http://localhost:5000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "coordenadas": [
      {"lat": -12.0464, "lon": -77.0428, "nombre": "Lima"},
      {"lat": -12.0565, "lon": -77.0538, "nombre": "Miraflores"}
    ],
    "n_clusters": 2,
    "metodo_tsp": "auto"
  }'
```

#### 3. Información de Algoritmos
```bash
curl http://localhost:5000/api/algorithms/info
```

### Frontend

1. Abrir `http://localhost:3000` en el navegador
2. Cargar dataset o usar datos de ejemplo
3. Configurar parámetros (número de clusters, método TSP)
4. Ejecutar optimización
5. Visualizar resultados

### Hito-2 (Standalone)

```python
from sistema_optimizacion import OptimizadorRutasHibrido
import numpy as np

# Crear coordenadas
coordenadas = np.array([
    [-12.0464, -77.0428],
    [-12.0565, -77.0538],
    # ... más puntos
])
nombres = ["Punto 1", "Punto 2", ...]

# Crear optimizador
optimizador = OptimizadorRutasHibrido(n_clusters=5)

# Ejecutar optimización
resultados = optimizador.optimizar(
    coordenadas, 
    nombres, 
    metodo_tsp='auto'
)

# Exportar resultados
optimizador.exportar_resultados('resultados.json')
```

## 🧪 Pruebas

### Backend
```bash
cd back
python test_api.py
```

### Frontend
```bash
cd sore
npm run lint
```

## 📊 Análisis de Complejidad

### Sin Optimización
- **Problema**: TSP sobre N puntos
- **Complejidad**: O(N!)
- **Límite práctico**: N ≤ 15

### Con Sistema Híbrido
- **Estrategia**: K-Means + TSP por cluster
- **Complejidad**: O(N + N²/K)
- **Escalable hasta**: N > 10,000

### Comparación

| N Puntos | Sin Optimizar | Con Híbrido (K=10) | Reducción |
|----------|---------------|-------------------|-----------|
| 10       | ~3.6M ops     | ~100 ops          | 36,000x   |
| 50       | Intratable    | ~2,500 ops        | ∞         |
| 100      | Imposible     | ~10,000 ops       | ∞         |
| 1000     | Imposible     | ~100,000 ops      | ∞         |

## 📚 Documentación Adicional

- [Hito-2 README](./Hito-2/README.md) - Detalles de algoritmos avanzados
- [Backend API README](./back/README.md) - Documentación completa de API
- [Frontend README](./sore/README.md) - Componentes y estructura

## 🔧 Configuración Avanzada

### Backend

Editar `back/.env`:
```env
FLASK_ENV=production
SECRET_KEY=tu-clave-secreta
MAX_CONTENT_LENGTH=16777216
PORT=5000
```

### Frontend

Editar `sore/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## 🐛 Solución de Problemas

### Backend no inicia
```bash
# Verificar Python
python --version

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Frontend no compila
```bash
# Limpiar cache
rm -rf .next node_modules
npm install
npm run dev
```

### Errores de CORS
- Verificar que el backend permite el origen del frontend en `config.py`
- Verificar que el frontend apunta al backend correcto

## 👥 Autores

**Grupo 03 - Complejidad Algorítmica**
- Universidad Peruana de Ciencias Aplicadas (UPC)
- Ciclo: 2024-2

## 📄 Licencia

Este proyecto es parte de un trabajo académico.

## 🙏 Agradecimientos

- Dataset proporcionado por Provías Nacional
- Librería scikit-learn para K-Means
- Next.js y Flask por los frameworks
- D3.js y vis-network para visualizaciones

## 📞 Soporte

Para problemas o preguntas:
1. Revisar la documentación en cada carpeta
2. Verificar los logs en consola
3. Consultar el documento `TF-Complejidad-Grupo03.md`

---

**🎓 Proyecto Académico - UPC 2024**

