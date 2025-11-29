"""
Script para demostrar la diferencia entre los algoritmos TSP
"""
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from tsp_algorithms import resolver_tsp

# Crear un conjunto de coordenadas de prueba (8 puntos)
np.random.seed(42)
coordenadas = np.array([
    [-12.046, -77.042],  # Lima centro
    [-12.050, -77.045],
    [-12.055, -77.040],
    [-12.048, -77.038],
    [-12.052, -77.043],
    [-12.049, -77.047],
    [-12.053, -77.041],
    [-12.047, -77.044]
])

print("=" * 70)
print("PRUEBA DE DIFERENCIAS ENTRE ALGORITMOS TSP")
print("=" * 70)
print(f"\nConjunto de prueba: {len(coordenadas)} puntos\n")

metodos = ['fuerza_bruta', 'backtracking', 'vecino_cercano']

resultados = []

for metodo in metodos:
    print(f"\n{'='*70}")
    print(f"EJECUTANDO: {metodo.upper()}")
    print(f"{'='*70}")

    ruta, distancia, stats = resolver_tsp(coordenadas, metodo=metodo)

    resultados.append({
        'metodo': metodo,
        'ruta': ruta,
        'distancia': distancia,
        'tiempo': stats['tiempo']
    })

    print(f"\n[RESULTADOS]")
    print(f"  Método: {stats['metodo']}")
    print(f"  Ruta: {ruta}")
    print(f"  Distancia: {distancia:.6f} km")
    print(f"  Tiempo: {stats['tiempo']:.6f} s")

    if 'permutaciones' in stats:
        print(f"  Permutaciones evaluadas: {stats['permutaciones']}")
    if 'nodos_explorados' in stats:
        print(f"  Nodos explorados: {stats['nodos_explorados']}")
    if 'podas' in stats:
        print(f"  Podas realizadas: {stats['podas']}")

print(f"\n{'='*70}")
print("COMPARACIÓN FINAL")
print(f"{'='*70}\n")

print(f"{'Método':<20} {'Distancia (km)':>15} {'Tiempo (s)':>12} {'Ruta'}")
print("-" * 70)

for r in resultados:
    ruta_str = str(r['ruta'][:5]) + '...' if len(r['ruta']) > 5 else str(r['ruta'])
    print(f"{r['metodo']:<20} {r['distancia']:>15.6f} {r['tiempo']:>12.6f} {ruta_str}")

print(f"\n{'='*70}")
print("ANÁLISIS")
print(f"{'='*70}\n")

# Comparar distancias
distancias = [r['distancia'] for r in resultados]
min_dist = min(distancias)
max_dist = max(distancias)

print(f"Distancia mínima: {min_dist:.6f} km")
print(f"Distancia máxima: {max_dist:.6f} km")
print(f"Diferencia: {max_dist - min_dist:.6f} km ({((max_dist - min_dist) / min_dist * 100):.2f}%)")

# Comparar tiempos
tiempos = [r['tiempo'] for r in resultados]
print(f"\nTiempo más rápido: {min(tiempos):.6f} s ({resultados[tiempos.index(min(tiempos))]['metodo']})")
print(f"Tiempo más lento: {max(tiempos):.6f} s ({resultados[tiempos.index(max(tiempos))]['metodo']})")

# Comparar rutas
print(f"\n¿Las rutas son diferentes?")
for i, r1 in enumerate(resultados):
    for j, r2 in enumerate(resultados):
        if i < j:
            son_iguales = r1['ruta'] == r2['ruta']
            print(f"  {r1['metodo']} vs {r2['metodo']}: {'IGUALES' if son_iguales else 'DIFERENTES'}")

print(f"\n{'='*70}")
print("CONCLUSIÓN")
print(f"{'='*70}\n")

if len(set(tuple(r['ruta']) for r in resultados)) == 1:
    print("[!] TODAS las rutas son IDÉNTICAS")
    print("    Los algoritmos están encontrando la misma solución.")
else:
    print("[OK] Las rutas son DIFERENTES")
    print("    Los algoritmos están funcionando de manera distinta.")

    # Verificar cuáles son óptimos
    mejor_distancia = min(distancias)
    for r in resultados:
        if abs(r['distancia'] - mejor_distancia) < 0.000001:
            print(f"    ✓ {r['metodo']} encontró la solución ÓPTIMA")
        else:
            pct_peor = ((r['distancia'] - mejor_distancia) / mejor_distancia * 100)
            print(f"    • {r['metodo']} es {pct_peor:.2f}% más largo (heurístico)")

print()

