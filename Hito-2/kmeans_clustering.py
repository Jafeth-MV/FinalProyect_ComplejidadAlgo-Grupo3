"""
K-Means Clustering Implementation
Algoritmo: Divide y Vencerás
Complejidad: O(n * k * i) donde n=puntos, k=clusters, i=iteraciones
"""

import numpy as np
from typing import List, Tuple
from sklearn.cluster import KMeans
import time


class KMeansClusterer:
    """
    Implementa K-Means clustering para dividir el problema TSP grande
    en subproblemas más pequeños y manejables.
    """

    def __init__(self, n_clusters: int = 5, random_state: int = 42):
        """
        Inicializa el clusterer.

        Args:
            n_clusters: Número de clusters a crear
            random_state: Semilla para reproducibilidad
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.model = None
        self.labels_ = None
        self.cluster_centers_ = None
        self.tiempo_ejecucion = 0

    def fit(self, coordenadas: np.ndarray) -> 'KMeansClusterer':
        """
        Ajusta el modelo K-Means a las coordenadas.

        Args:
            coordenadas: Array de coordenadas (N, 2) [lat, lon]

        Returns:
            self
        """
        inicio = time.time()

        # Crear y ajustar el modelo
        self.model = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=10,
            max_iter=300
        )

        self.model.fit(coordenadas)
        self.labels_ = self.model.labels_
        self.cluster_centers_ = self.model.cluster_centers_

        self.tiempo_ejecucion = time.time() - inicio

        return self

    def dividir_en_clusters(
        self,
        coordenadas: np.ndarray,
        nombres: List[str]
    ) -> List[Tuple[np.ndarray, List[str], List[int]]]:
        """
        Divide las coordenadas en clusters.

        Args:
            coordenadas: Array de coordenadas (N, 2)
            nombres: Lista de nombres de los puntos

        Returns:
            Lista de tuplas (coordenadas_cluster, nombres_cluster, indices_originales)
        """
        if self.labels_ is None:
            self.fit(coordenadas)

        clusters = []

        for i in range(self.n_clusters):
            # Obtener índices de puntos en este cluster
            indices = np.where(self.labels_ == i)[0]

            if len(indices) == 0:
                continue

            # Extraer coordenadas y nombres
            coords_cluster = coordenadas[indices]
            nombres_cluster = [nombres[idx] for idx in indices]

            clusters.append((coords_cluster, nombres_cluster, indices.tolist()))

        return clusters

    def obtener_estadisticas(self, coordenadas: np.ndarray) -> dict:
        """
        Calcula estadísticas del clustering.

        Args:
            coordenadas: Array de coordenadas

        Returns:
            Diccionario con estadísticas
        """
        if self.labels_ is None:
            return {}

        # Calcular tamaño de cada cluster
        tamanos = []
        for i in range(self.n_clusters):
            tamano = np.sum(self.labels_ == i)
            tamanos.append(tamano)

        # Calcular inercia (suma de distancias al cuadrado)
        inercia = self.model.inertia_ if self.model else 0

        return {
            'n_clusters': self.n_clusters,
            'tamanos_clusters': tamanos,
            'tamano_promedio': np.mean(tamanos),
            'tamano_max': np.max(tamanos),
            'tamano_min': np.min(tamanos),
            'inercia': float(inercia),
            'tiempo_ejecucion': self.tiempo_ejecucion,
            'centros': self.cluster_centers_.tolist() if self.cluster_centers_ is not None else []
        }

    def calcular_orden_clusters(self) -> List[int]:
        """
        Calcula un orden óptimo para visitar los clusters usando vecino más cercano.

        Returns:
            Lista de índices de clusters en orden
        """
        if self.cluster_centers_ is None:
            return list(range(self.n_clusters))

        n = len(self.cluster_centers_)
        visitados = [False] * n
        orden = []

        # Comenzar desde el cluster 0
        actual = 0
        orden.append(actual)
        visitados[actual] = True

        # Aplicar vecino más cercano
        for _ in range(n - 1):
            min_dist = float('inf')
            siguiente = -1

            for i in range(n):
                if not visitados[i]:
                    dist = np.linalg.norm(
                        self.cluster_centers_[actual] - self.cluster_centers_[i]
                    )
                    if dist < min_dist:
                        min_dist = dist
                        siguiente = i

            if siguiente != -1:
                orden.append(siguiente)
                visitados[siguiente] = True
                actual = siguiente

        return orden

