"""
TSP Algorithms Implementation
Implementa 3 algoritmos para el Problema del Viajero (TSP):
1. Fuerza Bruta - O(n!)
2. Backtracking con Poda - O(n!) optimizado
3. Vecino más Cercano - O(n²)
"""

import numpy as np
from itertools import permutations
import time
from typing import List, Tuple


def calcular_distancia(coord1: np.ndarray, coord2: np.ndarray) -> float:
    """
    Calcula la distancia euclidiana entre dos coordenadas.

    Args:
        coord1: Primera coordenada [lat, lon]
        coord2: Segunda coordenada [lat, lon]

    Returns:
        Distancia euclidiana
    """
    return np.linalg.norm(coord1 - coord2)


def calcular_distancia_total(coordenadas: np.ndarray, ruta: List[int]) -> float:
    """
    Calcula la distancia total de una ruta.

    Args:
        coordenadas: Array de coordenadas (N, 2)
        ruta: Lista de índices que representa la ruta

    Returns:
        Distancia total
    """
    distancia = 0
    for i in range(len(ruta) - 1):
        distancia += calcular_distancia(
            coordenadas[ruta[i]],
            coordenadas[ruta[i + 1]]
        )
    # Regresar al inicio
    distancia += calcular_distancia(
        coordenadas[ruta[-1]],
        coordenadas[ruta[0]]
    )
    return distancia


class TSPFuerzaBruta:
    """
    Resuelve TSP usando fuerza bruta.
    Complejidad: O(n!)
    Recomendado: n <= 10
    """

    def __init__(self):
        self.mejor_ruta = None
        self.mejor_distancia = float('inf')
        self.tiempo_ejecucion = 0
        self.permutaciones_evaluadas = 0

    def resolver(self, coordenadas: np.ndarray) -> Tuple[List[int], float]:
        """
        Resuelve TSP probando todas las permutaciones posibles.

        Args:
            coordenadas: Array de coordenadas (N, 2)

        Returns:
            Tupla (mejor_ruta, mejor_distancia)
        """
        n = len(coordenadas)

        if n > 10:
            raise ValueError(f"Fuerza bruta no recomendado para n={n} > 10")

        inicio = time.time()

        # Generar todas las permutaciones (excepto el punto inicial)
        puntos = list(range(n))
        inicio_fijo = puntos[0]
        resto = puntos[1:]

        self.mejor_distancia = float('inf')
        self.mejor_ruta = None
        self.permutaciones_evaluadas = 0

        # Probar todas las permutaciones
        for perm in permutations(resto):
            ruta = [inicio_fijo] + list(perm)
            distancia = calcular_distancia_total(coordenadas, ruta)

            self.permutaciones_evaluadas += 1

            if distancia < self.mejor_distancia:
                self.mejor_distancia = distancia
                self.mejor_ruta = ruta

        self.tiempo_ejecucion = time.time() - inicio

        return self.mejor_ruta, self.mejor_distancia


class TSPBacktracking:
    """
    Resuelve TSP usando backtracking con poda.
    Complejidad: O(n!) pero con optimización significativa
    Recomendado: n <= 15
    """

    def __init__(self):
        self.mejor_ruta = None
        self.mejor_distancia = float('inf')
        self.tiempo_ejecucion = 0
        self.nodos_explorados = 0
        self.podas_realizadas = 0

    def resolver(self, coordenadas: np.ndarray) -> Tuple[List[int], float]:
        """
        Resuelve TSP usando backtracking con poda.

        Args:
            coordenadas: Array de coordenadas (N, 2)

        Returns:
            Tupla (mejor_ruta, mejor_distancia)
        """
        n = len(coordenadas)

        if n > 15:
            raise ValueError(f"Backtracking no recomendado para n={n} > 15")

        inicio = time.time()

        self.mejor_distancia = float('inf')
        self.mejor_ruta = None
        self.nodos_explorados = 0
        self.podas_realizadas = 0

        # Iniciar backtracking desde el nodo 0
        visitados = [False] * n
        ruta_actual = [0]
        visitados[0] = True

        self._backtrack(coordenadas, visitados, ruta_actual, 0, n)

        self.tiempo_ejecucion = time.time() - inicio

        return self.mejor_ruta, self.mejor_distancia

    def _backtrack(
        self,
        coordenadas: np.ndarray,
        visitados: List[bool],
        ruta_actual: List[int],
        distancia_actual: float,
        n: int
    ):
        """
        Función recursiva de backtracking.
        """
        self.nodos_explorados += 1

        # Poda: si la distancia actual ya supera la mejor, no continuar
        if distancia_actual >= self.mejor_distancia:
            self.podas_realizadas += 1
            return

        # Caso base: todos los nodos visitados
        if len(ruta_actual) == n:
            # Agregar distancia de regreso al inicio
            distancia_total = distancia_actual + calcular_distancia(
                coordenadas[ruta_actual[-1]],
                coordenadas[ruta_actual[0]]
            )

            if distancia_total < self.mejor_distancia:
                self.mejor_distancia = distancia_total
                self.mejor_ruta = ruta_actual.copy()
            return

        # Probar cada nodo no visitado
        ultimo = ruta_actual[-1]

        for i in range(n):
            if not visitados[i]:
                # Calcular distancia al próximo nodo
                dist_adicional = calcular_distancia(
                    coordenadas[ultimo],
                    coordenadas[i]
                )

                # Poda temprana
                if distancia_actual + dist_adicional < self.mejor_distancia:
                    visitados[i] = True
                    ruta_actual.append(i)

                    self._backtrack(
                        coordenadas,
                        visitados,
                        ruta_actual,
                        distancia_actual + dist_adicional,
                        n
                    )

                    # Backtrack
                    ruta_actual.pop()
                    visitados[i] = False
                else:
                    self.podas_realizadas += 1


class TSPVecinoMasCercano:
    """
    Resuelve TSP usando heurística del vecino más cercano.
    Complejidad: O(n²)
    Recomendado: cualquier n (escalable)
    """

    def __init__(self):
        self.ruta = None
        self.distancia = 0
        self.tiempo_ejecucion = 0

    def resolver(self, coordenadas: np.ndarray, inicio: int = 0) -> Tuple[List[int], float]:
        """
        Resuelve TSP usando vecino más cercano.

        Args:
            coordenadas: Array de coordenadas (N, 2)
            inicio: Nodo inicial

        Returns:
            Tupla (ruta, distancia)
        """
        inicio_tiempo = time.time()

        n = len(coordenadas)
        visitados = [False] * n
        ruta = [inicio]
        visitados[inicio] = True
        distancia = 0

        actual = inicio

        # Construir la ruta
        for _ in range(n - 1):
            min_dist = float('inf')
            siguiente = -1

            # Encontrar el vecino más cercano no visitado
            for i in range(n):
                if not visitados[i]:
                    dist = calcular_distancia(coordenadas[actual], coordenadas[i])
                    if dist < min_dist:
                        min_dist = dist
                        siguiente = i

            if siguiente != -1:
                ruta.append(siguiente)
                visitados[siguiente] = True
                distancia += min_dist
                actual = siguiente

        # Regresar al inicio
        distancia += calcular_distancia(coordenadas[actual], coordenadas[inicio])

        self.ruta = ruta
        self.distancia = distancia
        self.tiempo_ejecucion = time.time() - inicio_tiempo

        return ruta, distancia


def seleccionar_algoritmo_tsp(n_puntos: int) -> str:
    """
    Selecciona el algoritmo TSP más apropiado según el número de puntos.

    Args:
        n_puntos: Número de puntos a optimizar

    Returns:
        Nombre del algoritmo recomendado
    """
    if n_puntos <= 10:
        return 'fuerza_bruta'
    elif n_puntos <= 15:
        return 'backtracking'
    else:
        return 'vecino_cercano'


def resolver_tsp(
    coordenadas: np.ndarray,
    metodo: str = 'auto'
) -> Tuple[List[int], float, dict]:
    """
    Resuelve TSP con el método especificado.

    Args:
        coordenadas: Array de coordenadas (N, 2)
        metodo: 'fuerza_bruta', 'backtracking', 'vecino_cercano', o 'auto'

    Returns:
        Tupla (ruta, distancia, estadisticas)
    """
    n = len(coordenadas)
    metodo_original = metodo
    advertencia = None

    # Selección automática solo si es 'auto'
    if metodo == 'auto':
        metodo = seleccionar_algoritmo_tsp(n)
    else:
        # Verificar si el método seleccionado es apropiado
        if metodo == 'fuerza_bruta' and n > 10:
            advertencia = f"ADVERTENCIA: Fuerza Bruta con {n} puntos puede ser muy lento (>{n}! operaciones)"
        elif metodo == 'backtracking' and n > 15:
            advertencia = f"ADVERTENCIA: Backtracking con {n} puntos puede tardar mucho tiempo"

    # Resolver según el método (FORZAR EL MÉTODO SELECCIONADO)
    if metodo == 'fuerza_bruta':
        solver = TSPFuerzaBruta()
        ruta, distancia = solver.resolver(coordenadas)
        stats = {
            'metodo': 'fuerza_bruta',
            'metodo_seleccionado': metodo_original,
            'tiempo': solver.tiempo_ejecucion,
            'permutaciones': solver.permutaciones_evaluadas
        }

    elif metodo == 'backtracking':
        solver = TSPBacktracking()
        ruta, distancia = solver.resolver(coordenadas)
        stats = {
            'metodo': 'backtracking',
            'metodo_seleccionado': metodo_original,
            'tiempo': solver.tiempo_ejecucion,
            'nodos_explorados': solver.nodos_explorados,
            'podas': solver.podas_realizadas
        }

    else:  # vecino_cercano
        solver = TSPVecinoMasCercano()
        ruta, distancia = solver.resolver(coordenadas)
        stats = {
            'metodo': 'vecino_cercano',
            'metodo_seleccionado': metodo_original,
            'tiempo': solver.tiempo_ejecucion
        }

    stats['n_puntos'] = n
    stats['distancia'] = distancia
    if advertencia:
        stats['advertencia'] = advertencia

    return ruta, distancia, stats

