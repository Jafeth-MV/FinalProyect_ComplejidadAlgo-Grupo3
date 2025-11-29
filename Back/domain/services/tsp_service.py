"""
TSP Algorithms Implementation
Refactored for DDD
"""

import numpy as np
from itertools import permutations
import time
from typing import List, Tuple, Dict, Any

class TSPService:
    @staticmethod
    def calculate_distance(coord1: np.ndarray, coord2: np.ndarray) -> float:
        # Haversine formula for single pair (fallback or single use)
        R = 6371.0
        lat1, lon1 = np.radians(coord1)
        lat2, lon2 = np.radians(coord2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        return R * c

    def _precompute_distance_matrix(self, coordinates: np.ndarray) -> np.ndarray:
        # Vectorized Haversine for N x N matrix
        R = 6371.0
        # Convert to radians
        coords_rad = np.radians(coordinates)
        lat = coords_rad[:, 0]
        lon = coords_rad[:, 1]
        
        # Broadcasting to get differences matrix (N x N)
        dlat = lat[:, np.newaxis] - lat
        dlon = lon[:, np.newaxis] - lon
        
        # Haversine formula vectorized
        a = np.sin(dlat / 2)**2 + np.cos(lat[:, np.newaxis]) * np.cos(lat) * np.sin(dlon / 2)**2
        # Clip to [0, 1] to avoid numerical errors with sqrt
        a = np.clip(a, 0, 1)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        
        return R * c

    @staticmethod
    def calculate_total_distance(dist_matrix: np.ndarray, ruta: List[int]) -> float:
        distancia = 0
        for i in range(len(ruta) - 1):
            distancia += dist_matrix[ruta[i], ruta[i+1]]
        distancia += dist_matrix[ruta[-1], ruta[0]]
        return distancia

    def solve(self, coordinates: np.ndarray, method: str = 'auto') -> Tuple[List[int], float, Dict[str, Any]]:
        n = len(coordinates)
        original_method = method
        warning = None

        if method == 'auto':
            if n <= 8:
                method = 'brute_force'
            elif n <= 12:
                method = 'backtracking'
            else:
                method = 'nearest_neighbor'
        
        if method == 'brute_force' and n > 8:
            warning = f"WARNING: Brute force with {n} points is slow."
        elif method == 'backtracking' and n > 12:
            warning = f"WARNING: Backtracking with {n} points is slow."

        start_time = time.time()
        stats = {'method': method, 'original_method': original_method}

        # Precompute distance matrix (O(N^2) but vectorized and fast)
        dist_matrix = self._precompute_distance_matrix(coordinates)

        if method == 'brute_force':
            route, distance = self._solve_brute_force(dist_matrix)
        elif method == 'backtracking':
            route, distance = self._solve_backtracking(dist_matrix, stats)
        elif method == 'kruskal':
            route, distance = self._solve_mst_tsp(dist_matrix)
        elif method == 'dijkstra':
            route, distance = self._solve_nearest_neighbor(dist_matrix)
        elif method == 'k_means':
             route, distance = self._solve_nearest_neighbor(dist_matrix)
        else:
            route, distance = self._solve_nearest_neighbor(dist_matrix)

        stats['execution_time'] = time.time() - start_time
        stats['n_points'] = n
        stats['distance'] = distance
        if warning:
            stats['warning'] = warning

        return route, distance, stats

    def _solve_brute_force(self, dist_matrix: np.ndarray) -> Tuple[List[int], float]:
        n = len(dist_matrix)
        points = list(range(n))
        start_node = points[0]
        rest = points[1:]
        
        best_dist = float('inf')
        best_route = None

        for perm in permutations(rest):
            route = [start_node] + list(perm)
            dist = self.calculate_total_distance(dist_matrix, route)
            if dist < best_dist:
                best_dist = dist
                best_route = route
        
        return best_route, best_dist

    def _solve_backtracking(self, dist_matrix: np.ndarray, stats: Dict) -> Tuple[List[int], float]:
        n = len(dist_matrix)
        self._best_dist_bt = float('inf')
        self._best_route_bt = None
        self._nodes_explored = 0
        self._prunes = 0

        visited = [False] * n
        current_route = [0]
        visited[0] = True

        self._backtrack_recursive(dist_matrix, visited, current_route, 0, n)
        
        stats['nodes_explored'] = self._nodes_explored
        stats['prunes'] = self._prunes
        return self._best_route_bt, self._best_dist_bt

    def _backtrack_recursive(self, dist_matrix, visited, current_route, current_dist, n):
        self._nodes_explored += 1
        if current_dist >= self._best_dist_bt:
            self._prunes += 1
            return

        if len(current_route) == n:
            total_dist = current_dist + dist_matrix[current_route[-1], current_route[0]]
            if total_dist < self._best_dist_bt:
                self._best_dist_bt = total_dist
                self._best_route_bt = current_route.copy()
            return

        last_node = current_route[-1]
        for i in range(n):
            if not visited[i]:
                dist_add = dist_matrix[last_node, i]
                if current_dist + dist_add < self._best_dist_bt:
                    visited[i] = True
                    current_route.append(i)
                    self._backtrack_recursive(dist_matrix, visited, current_route, current_dist + dist_add, n)
                    current_route.pop()
                    visited[i] = False
                else:
                    self._prunes += 1

    def _solve_nearest_neighbor(self, dist_matrix: np.ndarray) -> Tuple[List[int], float]:
        n = len(dist_matrix)
        visited = [False] * n
        route = [0]
        visited[0] = True
        distance = 0
        current = 0

        for _ in range(n - 1):
            min_dist = float('inf')
            next_node = -1
            
            # Vectorized search for nearest neighbor
            # Get row for current node
            row = dist_matrix[current]
            # Mask visited nodes with infinity
            masked_row = np.where(visited, float('inf'), row)
            
            next_node = np.argmin(masked_row)
            min_dist = masked_row[next_node]

            if min_dist == float('inf'):
                break # Should not happen if graph is complete

            route.append(next_node)
            visited[next_node] = True
            distance += min_dist
            current = next_node
        
        distance += dist_matrix[current, 0]
        return route, distance

    def _solve_mst_tsp(self, dist_matrix: np.ndarray) -> Tuple[List[int], float]:
        n = len(dist_matrix)
        if n <= 1:
            return [0], 0.0
            
        # 1. Build MST (Prim's Algorithm) using distance matrix
        key = [float('inf')] * n
        parent = [-1] * n
        key[0] = 0
        mst_set = [False] * n
        
        adj = {i: [] for i in range(n)}
        
        for _ in range(n):
            # Pick min key vertex
            # Simple linear scan O(N) -> Total O(N^2)
            u = -1
            min_val = float('inf')
            for v in range(n):
                if not mst_set[v] and key[v] < min_val:
                    min_val = key[v]
                    u = v
            
            if u == -1: break
            mst_set[u] = True
            
            if parent[u] != -1:
                adj[u].append(parent[u])
                adj[parent[u]].append(u)
                
            # Update adjacent vertices
            for v in range(n):
                if not mst_set[v]:
                    dist = dist_matrix[u, v]
                    if dist < key[v]:
                        key[v] = dist
                        parent[v] = u
                        
        # 2. DFS Preorder
        visited = [False] * n
        tour = []
        
        def dfs(u):
            visited[u] = True
            tour.append(u)
            for v in adj[u]:
                if not visited[v]:
                    dfs(v)
                    
        dfs(0)
        
        # 3. Calculate total distance
        total_dist = self.calculate_total_distance(dist_matrix, tour)
        return tour, total_dist
