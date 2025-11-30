# RutaFix: Sistema de Optimización de Rutas de Intervención Vial

**Proyecto de Complejidad Algorítmica - Grupo 03**

RutaFix es una plataforma diseñada para optimizar rutas de intervención vial utilizando algoritmos avanzados de teoría de grafos y heurísticas. El sistema permite gestionar grandes volúmenes de puntos de intervención, agruparlos eficientemente y calcular las rutas más cortas para las cuadrillas de trabajo.

---

## 🏗️ Arquitectura del Sistema (DDD)

El proyecto sigue una arquitectura basada en **Domain-Driven Design (DDD)** para desacoplar la lógica de negocio de la infraestructura y la interfaz de usuario.

### 1. Capa de Dominio (Domain)
*El núcleo del sistema. Contiene la lógica pura y las reglas de negocio.*
- **Modelos**: Definiciones de `Cluster`, `Route`, `Point`.
- **Servicios**:
    - `TSPService`: Implementa los algoritmos de resolución del problema del viajero (TSP).
    - `ClusteringService`: Se encarga de agrupar los puntos utilizando K-Means antes de la optimización.

### 2. Capa de Infraestructura (Infrastructure)
*Detalles técnicos y comunicación con el exterior.*
- **API**: Endpoints REST construidos con **FastAPI**.
- **Repositorios**: Manejo de lectura de datos desde archivos CSV y Excel (`FileRepository`).

### 3. Capa de Presentación (Frontend)
*Interfaz de usuario interactiva.*
- Construida con **React**, **TypeScript** y **Tailwind CSS**.
- Utiliza **Leaflet** para la visualización de mapas y rutas.

---

## 📂 Estructura del Proyecto

```mermaid
graph TD
    Root[📂 Proyecto] --> Back[📂 Back (Backend FastAPI)]
    Root --> Front[📂 Front (Frontend React)]

    subgraph Backend
    Back --> Domain[📂 domain]
    Back --> Infra[📂 infrastructure]
    
    Domain --> Services[📂 services]
    Infra --> API[📂 api]
    end

    subgraph Frontend
    Front --> Src[📂 src]
    Src --> Components[📂 components]
    Src --> App[App.tsx]
    end
```

### Guía de Archivos Clave

| Archivo | Ubicación | Descripción |
| :--- | :--- | :--- |
| **`tsp_service.py`** | `Back/domain/services/` | **Motor Algorítmico.** Contiene las implementaciones de Fuerza Bruta, Backtracking, Vecino Cercano y MST. |
| **`clustering_service.py`** | `Back/domain/services/` | **Agrupamiento.** Lógica de K-Means para dividir grandes conjuntos de puntos. |
| **`optimization.py`** | `Back/infrastructure/api/routers/` | **API Router.** Endpoint principal que orquesta la recepción de datos y la ejecución de algoritmos. |
| **`App.tsx`** | `Front/src/` | **Controlador UI.** Maneja el estado global, la barra lateral de configuración y la lógica de la aplicación. |
| **`MapView.tsx`** | `Front/src/components/` | **Visualizador.** Componente de mapa interactivo que renderiza clusters, rutas y marcadores. |

---

## 🧠 Algoritmos Implementados

El sistema ofrece múltiples estrategias para resolver el problema de enrutamiento (TSP), seleccionables manual o automáticamente:

| Algoritmo | Complejidad | Descripción |
| :--- | :---: | :--- |
| **Automático** | Variable | **Recomendado.** Selecciona la mejor estrategia según el número de puntos (`N`). <br>• `N <= 8`: Fuerza Bruta <br>• `N <= 12`: Backtracking <br>• `N > 12`: Vecino Más Cercano |
| **Fuerza Bruta** | `O(N!)` | Evalúa **todas** las permutaciones posibles. Garantiza la solución óptima absoluta pero es inviable para `N > 10`. |
| **Backtracking** | `O(N!)` | Similar a fuerza bruta pero con **poda**. Descarta ramas que ya superan la mejor distancia encontrada, mejorando el tiempo promedio. |
| **Vecino Más Cercano** | `O(N²)` | Heurística voraz (Greedy). En cada paso va al punto más cercano no visitado. Muy rápido y eficiente para grandes volúmenes. |
| **Kruskal (MST)** | `O(E log E)` | Aproximación basada en el Árbol de Expansión Mínima. Útil para estructuras de red. |

> **Nota sobre Clustering:** Para manejar miles de puntos, el sistema primero aplica **K-Means** para dividir el problema en sub-problemas (clusters) más pequeños, que luego son resueltos individualmente por el algoritmo TSP seleccionado.

---

## 🚀 Modos de Uso

La interfaz permite cuatro modos de operación distintos:

1.  **📅 Base CSV (Dataset)**
    *   Carga los datos históricos de intervenciones del MTC.
    *   Permite filtrar por fechas de corte (semestres).
    *   Ideal para visualizar la carga de trabajo real.

2.  **📤 Subir Excel**
    *   Permite al usuario cargar sus propios archivos `.xlsx` o `.csv`.
    *   **Formato requerido:** Columnas `Nombre`, `Latitud`, `Longitud`.

3.  **👆 Manual**
    *   Modo interactivo para pruebas rápidas.
    *   Haz clic directamente en el mapa para agregar puntos de destino.

4.  **🎲 Aleatorio**
    *   Genera puntos aleatorios en la región de Lima/Perú.
    *   Útil para pruebas de estrés y demostración de rendimiento.

---

## 🛠️ Instalación y Ejecución

### Requisitos Previos
- Python 3.8+
- Node.js 16+

### 1. Iniciar Backend

```bash
cd Back
# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
.\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn infrastructure.api.main:app --reload
```
*API disponible en: `http://localhost:8000`*

### 2. Iniciar Frontend

```bash
cd Front
# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```
*Aplicación disponible en: `http://localhost:5173`*

---

## 👥 Equipo

| Integrante | Rol |
| :--- | :--- |
| **Jafeth** | Lead Developer & Architect |
| **Grupo 03** | Algoritmos & QA |

---
*Desarrollado para el curso de Complejidad Algorítmica.*
