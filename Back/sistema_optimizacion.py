import numpy as np
from typing import List, Dict, Any, Optional
import time
import json

from kmeans_clustering import KMeansClusterer
from tsp_algorithms import resolver_tsp, calcular_distancia


class OptimizadorRutasHibrido:

    def __init__(self, n_clusters: int = 5, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.clusterer = KMeansClusterer(n_clusters, random_state)
        self.resultados = None

    def optimizar(
        self,
        coordenadas: np.ndarray,
        nombres: List[str],
        metodo_tsp: str = 'auto'
    ) -> Dict[str, Any]:
        inicio_total = time.time()

        # Paso 1: Clustering
        print(f"Aplicando K-Means con {self.n_clusters} clusters...")
        self.clusterer.fit(coordenadas)
        clusters = self.clusterer.dividir_en_clusters(coordenadas, nombres)
        stats_clustering = self.clusterer.obtener_estadisticas(coordenadas)

        print(f"Clusters creados: {len(clusters)}")
        for i, (coords, _, _) in enumerate(clusters):
            print(f"  Cluster {i}: {len(coords)} puntos")

        # Paso 2: Resolver TSP para cada cluster
        print(f"\nResolviendo TSP para cada cluster...")
        resultados_clusters = []
        tiempo_total_tsp = 0

        # Contador de métodos usados
        metodos_usados = {
            'fuerza_bruta': 0,
            'backtracking': 0,
            'vecino_cercano': 0,
            'unico_punto': 0
        }

        for i, (coords_cluster, nombres_cluster, indices_originales) in enumerate(clusters):
            n_puntos = len(coords_cluster)
            print(f"\n  Cluster {i} ({n_puntos} puntos):")

            if n_puntos == 1:
                # Solo un punto, no hay ruta
                ruta_local = [0]
                distancia = 0
                stats_tsp = {
                    'metodo': 'unico_punto',
                    'tiempo': 0,
                    'n_puntos': 1,
                    'distancia': 0
                }
                metodos_usados['unico_punto'] += 1
            else:
                # Resolver TSP - FORZAR EL MÉTODO SELECCIONADO
                print(f"    Método solicitado: {metodo_tsp}")
                ruta_local, distancia, stats_tsp = resolver_tsp(coords_cluster, metodo_tsp)
                tiempo_total_tsp += stats_tsp['tiempo']

                # Contar método usado
                metodo_real = stats_tsp.get('metodo', 'auto')
                if metodo_real in metodos_usados:
                    metodos_usados[metodo_real] += 1

                print(f"    Método ejecutado: {stats_tsp['metodo']}")
                print(f"    Distancia: {distancia:.4f}")
                print(f"    Tiempo: {stats_tsp['tiempo']:.4f}s")

                # Mostrar advertencia si existe
                if 'advertencia' in stats_tsp:
                    print(f"    {stats_tsp['advertencia']}")

            # Mapear ruta local a índices globales
            ruta_global = [indices_originales[idx] for idx in ruta_local]

            resultados_clusters.append({
                'cluster_id': i,
                'n_puntos': n_puntos,
                'ruta_local': ruta_local,
                'ruta_global': ruta_global,
                'distancia': distancia,
                'metodo': stats_tsp.get('metodo', 'auto'),
                'nombres': [nombres_cluster[idx] for idx in ruta_local],
                'coordenadas': coords_cluster[ruta_local].tolist(),
                'stats_tsp': stats_tsp
            })

        # Paso 3: Ordenar clusters
        print(f"\nOrdenando clusters...")
        orden_clusters = self.clusterer.calcular_orden_clusters()

        # Paso 4: Construir ruta global
        ruta_global_final = []
        distancia_total = 0
        distancia_entre_clusters = 0

        for idx_cluster in orden_clusters:
            cluster_result = resultados_clusters[idx_cluster]
            ruta_global_final.extend(cluster_result['ruta_global'])
            distancia_total += cluster_result['distancia']

        # Calcular distancias entre clusters
        for i in range(len(orden_clusters) - 1):
            idx_actual = orden_clusters[i]
            idx_siguiente = orden_clusters[i + 1]

            # Último punto del cluster actual
            ultimo_punto_actual = resultados_clusters[idx_actual]['ruta_global'][-1]
            # Primer punto del siguiente cluster
            primer_punto_siguiente = resultados_clusters[idx_siguiente]['ruta_global'][0]

            dist = calcular_distancia(
                coordenadas[ultimo_punto_actual],
                coordenadas[primer_punto_siguiente]
            )
            distancia_entre_clusters += dist

        # Distancia de regreso al inicio
        if len(ruta_global_final) > 0:
            dist_regreso = calcular_distancia(
                coordenadas[ruta_global_final[-1]],
                coordenadas[ruta_global_final[0]]
            )
            distancia_entre_clusters += dist_regreso

        distancia_total += distancia_entre_clusters

        tiempo_total = time.time() - inicio_total

        # Construir resultado completo
        self.resultados = {
            'ruta_global': ruta_global_final,
            'distancia_total': distancia_total,
            'distancia_dentro_clusters': distancia_total - distancia_entre_clusters,
            'distancia_entre_clusters': distancia_entre_clusters,
            'n_puntos_total': len(coordenadas),
            'n_clusters': len(clusters),
            'orden_clusters': orden_clusters,
            'clusters': resultados_clusters,
            'estadisticas': {
                'tiempo_total': tiempo_total,
                'tiempo_clustering': stats_clustering['tiempo_ejecucion'],
                'tiempo_tsp': tiempo_total_tsp,
                'clustering': stats_clustering,
                'metodo_tsp': metodo_tsp,
                'metodos_usados': metodos_usados
            }
        }

        # Imprimir resumen
        print(f"\n" + "="*60)
        print(f"RESUMEN DE OPTIMIZACIÓN")
        print(f"="*60)
        print(f"Puntos totales: {len(coordenadas)}")
        print(f"Clusters: {len(clusters)}")
        print(f"Distancia total: {distancia_total:.4f}")
        print(f"  - Dentro de clusters: {distancia_total - distancia_entre_clusters:.4f}")
        print(f"  - Entre clusters: {distancia_entre_clusters:.4f}")
        print(f"Tiempo total: {tiempo_total:.4f}s")
        print(f"  - Clustering: {stats_clustering['tiempo_ejecucion']:.4f}s")
        print(f"  - TSP: {tiempo_total_tsp:.4f}s")
        print(f"="*60)

        return self.resultados

    def obtener_ruta_nombres(self) -> List[str]:
        if self.resultados is None:
            return []

        nombres_ordenados = []
        for cluster_id in self.resultados['orden_clusters']:
            cluster = self.resultados['clusters'][cluster_id]
            nombres_ordenados.extend(cluster['nombres'])

        return nombres_ordenados

    def exportar_resultados(self, archivo: str = 'resultados_optimizacion.json'):
        if self.resultados is None:
            print("No hay resultados para exportar")
            return

        # Convertir arrays numpy a listas para JSON
        resultados_json = self._preparar_para_json(self.resultados)

        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(resultados_json, f, indent=2, ensure_ascii=False)

        print(f"Resultados exportados a: {archivo}")

    def _preparar_para_json(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, dict):
            return {key: self._preparar_para_json(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._preparar_para_json(item) for item in obj]
        else:
            return obj
