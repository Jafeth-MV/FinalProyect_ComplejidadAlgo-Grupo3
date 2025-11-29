# 🚀 RutaFix: Sistema de Optimización de Rutas de Intervención Vial

![Status](https://img.shields.io/badge/Estado-Completado-success)
![Version](https://img.shields.io/badge/Versión-2.0-blue)
![Tech](https://img.shields.io/badge/Stack-FastAPI%20%7C%20React%20%7C%20Leaflet-orange)

**Proyecto de Complejidad Algorítmica - Grupo 03**  
Universidad Peruana de Ciencias Aplicadas (UPC) - 2024-2

---

## 📖 Descripción General

**RutaFix** es una plataforma avanzada para la planificación y optimización de rutas de mantenimiento vial en el Perú. Utiliza algoritmos de **Inteligencia Artificial** y **Teoría de Grafos** para minimizar distancias y tiempos de traslado entre puntos de intervención.

El sistema procesa miles de registros reales, los agrupa inteligentemente mediante **Clustering (K-Means)** y resuelve el problema del viajante (TSP) utilizando una estrategia híbrida de algoritmos (**Fuerza Bruta, Backtracking y Vecino Más Cercano**).

---

## 🏗️ Arquitectura del Sistema (DDD)

El proyecto sigue los principios de **Domain-Driven Design (DDD)** para garantizar un código limpio, escalable y mantenible.

### 🧩 Capas del Sistema

1.  **🟡 Dominio (Domain)**
    *   *El corazón del negocio.* Aquí viven las reglas y entidades puras.
    *   **Modelos**: `Cluster`, `Route`, `Point`.
    *   **Servicios**: Lógica de algoritmos TSP (`TSPService`) y Clustering (`ClusteringService`).
    *   *No depende de nadie, todos dependen de él.*

2.  **🔵 Infraestructura (Infrastructure)**
    *   *Los detalles técnicos.* Implementaciones concretas y conexiones externas.
    *   **Repositorios**: Carga de datos desde CSV (`FileRepository`).
    *   **API**: Endpoints REST con FastAPI (`routers`).

3.  **🟢 Aplicación (Application)**
    *   *La orquestación.* Conecta el mundo exterior con el dominio.
    *   **Casos de Uso**: Coordinan la ejecución de clustering y optimización.

---

## 📂 Estructura Interactiva del Proyecto

Explora cómo se relacionan los archivos principales:

```mermaid
graph TD
    Root[📂 Proyecto] --> Back[📂 Back (Backend FastAPI)]
    Root --> Front[📂 Front (Frontend React)]

    subgraph Backend
    Back --> Infra[📂 infrastructure]
    Back --> Domain[📂 domain]
    
    Infra --> API[📂 api]
    Infra --> Repos[📂 repositories]
    
    Domain --> Models[📂 models]
    Domain --> Services[📂 services]
    end

    subgraph Frontend
    Front --> Components[📂 components]
    Front --> ServicesFront[📂 services]
    end
```

### 📜 Guía de Archivos Clave

| Archivo / Carpeta | Capa (DDD) | ¿Qué hace? |
| :--- | :---: | :--- |
| **`Back/domain/services/tsp_service.py`** | 🟡 Dominio | **El Cerebro.** Contiene los algoritmos TSP (Fuerza Bruta, Backtracking, Vecino Cercano). |
| **`Back/domain/services/clustering_service.py`** | 🟡 Dominio | **El Organizador.** Divide miles de puntos en grupos (clusters) usando K-Means. |
| **`Back/infrastructure/api/routers/optimization.py`** | 🔵 Infra | **El Controlador.** Recibe las peticiones del Frontend y devuelve las rutas optimizadas. |
| **`Back/infrastructure/repositories/data_loader.py`** | 🔵 Infra | **El Cargador.** Lee y procesa el archivo CSV masivo de intervenciones. |
| **`Front/src/components/MapView.tsx`** | 🎨 UI | **El Mapa.** Componente principal que dibuja rutas, clusters y maneja la interacción visual. |
| **`Front/src/components/Sidebar.tsx`** | 🎨 UI | **El Panel.** Menú lateral para configurar algoritmos, fechas y modos de uso. |

---

## ⚡ Algoritmos y Rendimiento

El sistema selecciona automáticamente el mejor algoritmo según la complejidad del problema:

| Algoritmo | Complejidad | Uso Ideal | ¿Por qué? |
| :--- | :---: | :--- | :--- |
| **Fuerza Bruta** | `O(n!)` | `n <= 8` | Garantiza la ruta **perfecta** probando todas las combinaciones. |
| **Backtracking (Poda)** | `O(n!)` | `n <= 12` | Inteligente. Corta caminos que ya son peores que el mejor encontrado. |
| **Vecino Más Cercano** | `O(n²)` | `n > 12` | **Velocidad extrema.** Para grandes volúmenes, da una solución muy buena en milisegundos. |

> **🚀 Optimización K-Means:** Al dividir 100 puntos en 10 clusters de 10, pasamos de un problema imposible `O(100!)` a 10 problemas triviales `O(10!)`. ¡Divide y vencerás!

---

## 🛠️ Instalación y Uso

### 1️⃣ Backend (Python/FastAPI)

```bash
cd Back
pip install -r requirements.txt
uvicorn infrastructure.api.main:app --reload
```
*El servidor iniciará en `http://localhost:8000`*

### 2️⃣ Frontend (React/Vite)

```bash
cd Front
npm install
npm run dev
```
*La web abrirá en `http://localhost:5173`*

---

## 🎮 Modos de Uso

1.  **📂 Modo CSV**: Carga la base de datos real. Filtra por semestres y visualiza miles de intervenciones.
2.  **🎲 Modo Aleatorio**: Genera puntos en la **Macro Región Centro-Sur (Trujillo a Nazca)**. ¡Prueba la escalabilidad!
3.  **✍️ Modo Manual**: Haz clic en el mapa para crear tus propios puntos y planificar una ruta personalizada.
4.  **📤 Carga Propia**: Sube tu propio Excel/CSV con direcciones.

---

## 👥 Equipo de Desarrollo

| Integrante | Rol |
| :--- | :--- |
| **Jafeth** | Lead Developer & Architect |
| **Grupo 03** | Algoritmos & QA |

---
*Desarrollado con ❤️ y mucho café para el curso de Complejidad Algorítmica.*
