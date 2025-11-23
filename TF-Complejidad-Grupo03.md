Introducción
En el contexto urbano de Lima Metropolitana, la gestión eficiente de las intervenciones técnicas y domiciliarias (mantenimiento de servicios, reparaciones, visitas técnicas) representa un desafío logístico de gran impacto operativo y económico. Los tiempos de traslado de los equipos técnicos son determinantes para la calidad del servicio, el cumplimiento de las citas y la eficiencia en el uso de recursos. Sin embargo, factores como la severa congestión vehicular, la complejidad de la red vial y la falta de herramientas de planificación automatizada dificultan alcanzar este objetivo de manera sistemática.
El presente trabajo, denominado "RutaFix", propone una solución basada en la Complejidad Algorítmica y el modelado de grafos. En este enfoque, la red vial se representa como un grafo ponderado donde las intersecciones y puntos de control son nodos, y los tramos viales son aristas con pesos asociados a la distancia o tiempo de recorrido. A partir de este modelo, se aplicarán algoritmos de optimización, clustering y búsqueda de rutas con el propósito de determinar las trayectorias más eficientes para las cuadrillas técnicas, reduciendo así los tiempos de traslado, el consumo de combustible y equilibrando la carga laboral.
1.1. Objetivo del trabajo
Desarrollar un modelo computacional que, mediante el uso de algoritmos de complejidad algorítmica (como Dijkstra, K-Means y heurísticas para el TSP), permita calcular y optimizar las rutas de visita para equipos técnicos en Lima Metropolitana. El modelo busca minimizar la distancia total recorrida, reducir los tiempos de respuesta ante solicitudes de servicio y demostrar la aplicabilidad práctica de las estructuras de datos avanzadas en la resolución de problemas logísticos reales.
1.2. Alcance
Para delimitar el desarrollo de la solución "RutaFix", se han establecido los siguientes alcances y restricciones:
Representación del Modelo: El sistema se enfoca en la representación de la red vial de Lima Metropolitana (específicamente rutas departamentales y vecinales) como un grafo ponderado, utilizando el dataset oficial de Provías Descentralizado.
Funcionalidad Algorítmica: Se implementarán y compararán algoritmos de particionamiento (K-Means para dividir zonas de trabajo), optimización combinatoria (Fuerza Bruta/Heurísticas para el orden de visitas) y búsqueda de caminos mínimos (Dijkstra) para validar su eficiencia computacional.
Visualización: Los resultados y rutas calculadas se mostrarán mediante una interfaz gráfica que permita visualizar los clústeres asignados y el trazado sobre un mapa interactivo.
Limitaciones: El trabajo se limita a una simulación académica utilizando datos estáticos (archivos CSV geocodificados); no contempla la integración en tiempo real con APIs de tráfico en vivo (como Google Traffic o Waze) ni la gestión dinámica de flotas en movimiento para esta etapa.

2.  Descripción del problema

2.1. Fundamentación del problema

En el ámbito de la logística de servicios en Lima Metropolitana, la planificación de rutas para equipos técnicos (mantenimiento, instalaciones, reparaciones) se realiza, en gran medida, de manera empírica o asistida por herramientas básicas que no consideran la optimización global de la flota. Los despachadores o los mismos técnicos deciden el orden de las visitas basándose en la intuición geográfica, lo cual, en una ciudad con una trama urbana densa y compleja, resulta en trayectorias sub-óptimas.
Este enfoque manual genera ineficiencias críticas: tiempos muertos excesivos entre visitas, recorridos redundantes ("ir y volver" por la misma zona) y una distribución desequilibrada de la carga de trabajo entre las cuadrillas. Desde una perspectiva computacional, este escenario corresponde a una variación del Problema de Enrutamiento de Vehículos (VRP) y el Problema del Viajante (TSP), los cuales pertenecen a la clase de problemas de optimización combinatoria NP-hard. A medida que aumenta el número de puntos de visita (N), la cantidad de rutas posibles crece factorialmente (N!), haciendo imposible para un operador humano encontrar la solución óptima sin asistencia algorítmica.
2.2. Contexto y relevancia

El contexto urbano de Lima agrava la problemática anterior. La ciudad presenta altos índices de congestión vehicular y una infraestructura vial heterogénea, donde la distancia euclidiana (línea recta) rara vez refleja el costo real del desplazamiento. En este escenario, la falta de una planificación optimizada tiene consecuencias directas en tres dimensiones:
Impacto Económico: El exceso de kilometraje recorrido se traduce directamente en un mayor gasto de combustible y desgaste de vehículos, incrementando los costos operativos de las empresas de servicios.
Calidad del Servicio: Los retrasos acumulados por rutas ineficientes provocan incumplimiento de las ventanas horarias prometidas al cliente final, deteriorando la percepción del servicio.
Impacto Ambiental: Rutas más largas implican mayores emisiones de CO2, contribuyendo a la huella de carbono de la ciudad.
Por tanto, la relevancia de este proyecto trasciende la mera aplicación teórica; busca proponer una solución tecnológica que utilice la Complejidad Algorítmica para transformar un problema logístico intratable manualmente en un proceso eficiente, escalable y sostenible.
3.  Descripción del Conjunto de Datos (Dataset)

3.1. Origen y características de los datos
El conjunto de datos base utilizado para este proyecto proviene de la plataforma de Datos Abiertos del Gobierno del Perú, específicamente de la colección gestionada por Provías Descentralizado (Ministerio de Transportes y Comunicaciones).
Fuente: "Intervenciones en Redes Viales Subnacionales (Redes Viales Departamentales y Vecinales del Sistema Nacional de Carret1111111111111eras)".
Cobertura Geográfica: El dataset original cubre todo el territorio nacional. Para efectos de este proyecto, se realizó un filtrado específico para obtener los registros correspondientes a Lima Metropolitana, asegurando un volumen de datos que cumpla con el requisito mínimo de complejidad (más de 1,500 nodos).
Las características (atributos) principales seleccionadas para el modelado son:
Código de ruta y tramo: Identificador único que permite diferenciar cada segmento vial.
Longitud (km): Distancia física del tramo, dato base para el peso de las aristas.
Superficie de rodadura: Tipo de material (asfalto, afirmado, tierra), útil para calcular velocidades promedio.
Estado de conservación: Condición actual de la vía (Bueno, Regular, Malo), utilizado como factor de penalización en el cálculo de tiempos.
Ubicación textual: Información de "Trayectoria", "Inicio" y "Fin" en formato de texto (ej. "Emp. PE-1S - Canta").
3.2. Representación mediante grafo


















2. Descripción del conjunto de datos (dataset)
   2.1. Descripción del Dataset
   El dataset utilizado proviene de Provías Descentralizado (Ministerio de Transportes y Comunicaciones del Perú), en la colección:
   “Intervenciones en Redes Viales Subnacionales (Redes Viales Departamentales y Vecinales del Sistema Nacional de Carreteras)” Fuente oficial: Gobierno del Perú – Datos Abiertos
   Características principales:
   Código de ruta y tramo: identificador único de cada carretera.
   Longitud (km): distancia total de cada segmento.
   Superficie de rodadura: tipo de material (asfalto, afirmado, tierra).
   Estado de conservación: condición actual del tramo (bueno, regular, malo).
   Ubicación geográfica: información por departamento, provincia y distrito.
   Para el caso de Lima Metropolitana, se filtraron los registros correspondientes a las rutas departamentales y vecinales, lo que permitió modelar una red vial de más de 1,500 nodos y 2,000 aristas, cumpliendo con los requisitos mínimos del trabajo.
   Representación como grafo:
   Nodos (V): puntos iniciales y finales de cada tramo de carretera.
   Aristas (E): conexiones entre los nodos con pesos basados en la longitud o tiempo estimado.
   Pesos dinámicos: en escenarios simulados se ajustan considerando el estado de la vía (ejemplo: una vía en mal estado aumenta el tiempo de recorrido).
   2.2. Pre-procesamiento y Geocodificación del Dataset
   El dataset original de Provías Descentralizado provee información textual de las intervenciones, como TRAMO, PROVINCIA y DEPARTAMENTO, pero no incluye coordenadas geográficas (latitud, longitud) explícitas.
   Para construir un grafo espacial y calcular distancias reales, es necesario un paso de geocodificación. Este proceso consiste en convertir las direcciones textuales (ej. "Tramo X, Provincia Y, Lima") en coordenadas (latitud, longitud).
   Para este fin, se utilizará la biblioteca geopy de Python (vista en el notebook de implementación) para consultar un servicio como Nominatim (basado en OpenStreetMap). Este paso es fundamental para generar los nodos del grafo en sus ubicaciones reales y, posteriormente, calcular la matriz de distancias (pesos de las aristas) usando la fórmula de Haversine (distancia en una esfera).

Además, se construyó un subgrafo correspondiente al distrito de San Juan de Lurigancho, como ejemplo de caso de uso en un área más acotada y manejable.

3. Propuesta y Metodología
   El proyecto RutaFix busca optimizar las rutas de técnicos que realizan intervenciones domiciliarias y de mantenimiento en Lima, utilizando la red vial real como base de simulación.
   3.1. Objetivos de la Propuesta
   Reducir el tiempo total de recorrido de los técnicos.
   Minimizar el consumo de combustible y la huella ambiental.
   Garantizar un mejor equilibrio en la asignación de visitas por técnico.
   Aplicar de manera práctica los algoritmos de complejidad algorítmica en un caso real.
   3.2. Metodología de Optimización
   La solución "RutaFix" se implementará siguiendo una metodología híbrida que combina técnicas de clustering y algoritmos de grafos para abordar el Problema de Rutas de Vehículos (VRP):
   Fase 1: Particionamiento (Divide y Vencerás): Dado que un grafo de +1500 nodos es intratable con Fuerza Bruta (complejidad O(n!)), el primer paso es aplicar un algoritmo de Divide y Vencerás. Se usará el algoritmo de clustering K-Means (implementado en el notebook) para agrupar los N puntos de intervención en K zonas geográficas (clústeres) más pequeñas y manejables.
   Fase 2: Resolución Intra-Clúster (Fuerza Bruta / Heurística): Una vez que los nodos están agrupados, el problema se reduce a encontrar la ruta óptima dentro de cada clúster.
   Para clústeres muy pequeños (ej. n ≤ 10), se puede aplicar Fuerza Bruta (TSP) para garantizar la ruta óptima.
   Para clústeres más grandes, se usará una heurística eficiente como la del "Vecino más Cercano" (implementada en el notebook como vecino) para encontrar una solución "suficientemente buena" en tiempo polinomial (ej. O(n²)).
   Fase 3: Cálculo de Rutas Específicas (Dijkstra): Para calcular la ruta más corta entre dos puntos específicos del grafo (ej. desde el almacén central hasta el primer punto de un clúster), se utilizará el algoritmo de Dijkstra. Este algoritmo es ideal para encontrar el camino mínimo en grafos ponderados como nuestra red vial.
   3.3. Validación
   La efectividad de la propuesta se medirá mediante:
   Comparación: Rutas manuales (línea base) vs. rutas optimizadas por "RutaFix".
   Métricas: Distancia total (km), tiempo estimado (min) y tiempo de cómputo (s).
   Simulación: Pruebas con diferentes tamaños de dataset (50, 200, 500 nodos)
4. Diseño del aplicativo
   El diseño del aplicativo se describe considerando tanto su arquitectura de software como el análisis de los algoritmos implementados.
   4.1. Arquitectura de la Solución
   El aplicativo "RutaFix" se diseña bajo una arquitectura modular en Python, facilitando la implementación y pruebas. Los componentes principales son:
   Módulo 1: Carga y Procesamiento de Datos: Lee el archivo .csv de Provías. Es responsable de filtrar las columnas relevantes (ej. TRAMO, PROVINCIA) y manejar los datos faltantes.


Módulo 2: Geocodificación y Modelado de Grafo: Utiliza la biblioteca geopy para convertir las direcciones textuales en coordenadas (lat, lon), como se detalló en la sección 2.2. Luego, construye la matriz de adyacencia ponderada. El peso W(u, v) entre dos nodos es la distancia geodésica (fórmula de Haversine).


Módulo 3: Núcleo de Algoritmos: Contiene la lógica central de optimización:
KMeans (de scikit-learn) para el clustering (Divide y Vencerás).
tsp_bruto (Fuerza Bruta) y vecino (Heurística del Vecino más Cercano) para la optimización intra-clúster.
dijkstra_adjlist (Dijkstra) para el cálculo de rutas específicas A-B.


Módulo 4: Interfaz Gráfica (GUI): El enunciado del trabajo solicita una demostración de la aplicación en una interfaz gráfica. Se diseñará una interfaz simple (por ejemplo, usando Streamlit o Folium) que permita al usuario:


Cargar el dataset.
Seleccionar un conjunto de puntos (o un clúster) a visitar.
Visualizar en un mapa la ruta no optimizada (línea base) vs. la ruta optimizada por "RutaFix".
Calcular la ruta más corta entre dos puntos A y B usando Dijkstra.
4.2. Análisis de Algoritmos Aplicados
Fuerza Bruta (TSP):
Descripción: Explora todas las n! permutaciones de visitas posibles para encontrar la de menor costo.


Análisis de Complejidad: Su complejidad temporal es O(n!). Es computacionalmente inviable para problemas que excedan ~10-12 nodos. Su uso en este proyecto se limita a validar la optimalidad en sub-problemas muy pequeños.


Divide y Vencerás (Clustering + Heurística):
Descripción: Reduce la complejidad partiendo el problema de N nodos en Ksub-problemas de tamaño  ≈N/K. Se usa K-Means para la partición y la heurística del "Vecino más Cercano" para la resolución de cada sub-problema.


Análisis de Complejidad: La heurística del Vecino más Cercano es O(n²). Al resolver K problemas de tamaño = N/K , la complejidad total (ej. K * (N/K)² = N²/K) es drásticamente menor que  O(N!), permitiendo escalar la solución.


Algoritmo de Dijkstra:


Descripción: Encuentra el camino de costo mínimo desde un nodo origen a todos los demás nodos en un grafo ponderado.


Análisis de Complejidad: La implementación utiliza una cola de prioridad (heapq). Su complejidad temporal es O(E log V), donde V es el número de nodos y E el de aristas. Es altamente eficiente para encontrar rutas específicas en nuestra red vial.
5. Anexos
   Código fuente en Python para la lectura del dataset, construcción del grafo y ejecución de algoritmos.
   Capturas de mapas con rutas calculadas.
   Reportes en CSV de métricas comparativas (baseline vs optimizado).
