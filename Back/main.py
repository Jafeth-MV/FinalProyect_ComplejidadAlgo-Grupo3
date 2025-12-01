import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from dataset_processor import DatasetProcessor
from sistema_optimizacion import OptimizadorRutasHibrido


def visualizar_resultados(coordenadas, nombres, resultados, archivo='clusters_visualizacion.png'):
    print(f"\nGenerando visualización...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Colores para cada cluster
    colores = plt.cm.tab10(np.linspace(0, 1, len(resultados['clusters'])))

    # Subplot 1: Clusters
    ax1.set_title('Clusters K-Means', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Longitud')
    ax1.set_ylabel('Latitud')

    for i, cluster in enumerate(resultados['clusters']):
        indices = cluster['ruta_global']
        coords_cluster = coordenadas[indices]

        # Puntos del cluster
        ax1.scatter(
            coords_cluster[:, 1],
            coords_cluster[:, 0],
            c=[colores[i]],
            s=100,
            alpha=0.6,
            label=f'Cluster {i} ({len(indices)} pts)'
        )

        # Etiquetar primer punto de cada cluster
        if len(coords_cluster) > 0:
            ax1.annotate(
                f'C{i}',
                (coords_cluster[0, 1], coords_cluster[0, 0]),
                fontsize=8,
                fontweight='bold'
            )

    # Centros de clusters
    if 'clustering' in resultados['estadisticas']:
        centros = np.array(resultados['estadisticas']['clustering']['centros'])
        ax1.scatter(
            centros[:, 1],
            centros[:, 0],
            c='red',
            s=300,
            marker='X',
            edgecolors='black',
            linewidth=2,
            label='Centros',
            zorder=5
        )

    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)

    # Subplot 2: Ruta optimizada
    ax2.set_title('Ruta Optimizada', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Longitud')
    ax2.set_ylabel('Latitud')

    # Dibujar ruta completa
    ruta_global = resultados['ruta_global']
    coords_ruta = coordenadas[ruta_global]

    # Líneas conectando los puntos
    for i in range(len(coords_ruta)):
        j = (i + 1) % len(coords_ruta)
        ax2.plot(
            [coords_ruta[i, 1], coords_ruta[j, 1]],
            [coords_ruta[i, 0], coords_ruta[j, 0]],
            'b-',
            alpha=0.3,
            linewidth=1
        )

    # Puntos coloreados por cluster
    for i, cluster in enumerate(resultados['clusters']):
        indices = cluster['ruta_global']
        coords_cluster = coordenadas[indices]

        ax2.scatter(
            coords_cluster[:, 1],
            coords_cluster[:, 0],
            c=[colores[i]],
            s=100,
            alpha=0.6,
            label=f'Cluster {i}'
        )

    # Marcar inicio
    ax2.scatter(
        coords_ruta[0, 1],
        coords_ruta[0, 0],
        c='green',
        s=300,
        marker='*',
        edgecolors='black',
        linewidth=2,
        label='Inicio',
        zorder=5
    )

    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(archivo, dpi=150, bbox_inches='tight')
    print(f"Visualización guardada: {archivo}")
    plt.close()


def main():
    print("="*70)
    print("SISTEMA DE OPTIMIZACION DE RUTAS DE EVACUACION")
    print("="*70)
    print("Algoritmos: K-Means + TSP (Fuerza Bruta/Backtracking/Vecino Cercano)")
    print("="*70)
    print()

    # Configuración
    ARCHIVO_DATASET = 'dataset_tp_complejidad.xlsx'
    ARCHIVO_CSV = '1_Dataset_Intervenciones_PVD_30062025.csv'
    MAX_PUNTOS = 50  # Limitar para demostración
    N_CLUSTERS = 5

    # MENU INTERACTIVO PARA ELEGIR ALGORITMO TSP
    print("\n" + "="*70)
    print("SELECCION DE ALGORITMO TSP")
    print("="*70)
    print("\nElija el algoritmo TSP a utilizar:\n")
    print("  1. Fuerza Bruta       - O(n!) - Garantiza solucion optima (n <= 10)")
    print("  2. Backtracking       - O(n!) con poda - Optimo con poda (n <= 15)")
    print("  3. Vecino mas Cercano - O(n^2) - Heuristico, rapido y escalable")
    print("  4. Automatico         - El sistema elige segun el tamano (RECOMENDADO)")
    print("\n" + "="*70)

    while True:
        try:
            opcion = input("\nIngrese su opcion (1-4): ").strip()
            if opcion == '1':
                METODO_TSP = 'fuerza_bruta'
                print("\n[OK] Algoritmo seleccionado: FUERZA BRUTA")
                break
            elif opcion == '2':
                METODO_TSP = 'backtracking'
                print("\n[OK] Algoritmo seleccionado: BACKTRACKING")
                break
            elif opcion == '3':
                METODO_TSP = 'vecino_cercano'
                print("\n[OK] Algoritmo seleccionado: VECINO MAS CERCANO")
                break
            elif opcion == '4':
                METODO_TSP = 'auto'
                print("\n[OK] Algoritmo seleccionado: AUTOMATICO")
                break
            else:
                print("[ERROR] Opcion invalida. Ingrese 1, 2, 3 o 4.")
        except KeyboardInterrupt:
            print("\n\n[INFO] Operacion cancelada. Usando modo AUTOMATICO.")
            METODO_TSP = 'auto'
            break

    print("\n" + "="*70)

    # Paso 1: Cargar o generar dataset
    processor = DatasetProcessor()

    # Intentar cargar desde Excel primero
    if os.path.exists(ARCHIVO_DATASET):
        print(f"Cargando dataset desde archivo Excel...")
        try:
            coordenadas, nombres = processor.cargar_desde_excel(ARCHIVO_DATASET)

            # Limitar puntos si hay muchos
            if len(coordenadas) > MAX_PUNTOS:
                coordenadas, nombres = processor.limitar_puntos(MAX_PUNTOS)

        except Exception as e:
            print(f"Error al cargar Excel: {e}")
            coordenadas, nombres = None, None

    # Si no hay Excel, intentar cargar desde CSV
    if coordenadas is None and os.path.exists(ARCHIVO_CSV):
        print(f"Cargando dataset desde CSV de intervenciones...")
        try:
            coordenadas, nombres = processor.cargar_desde_csv_intervenciones(
                ARCHIVO_CSV,
                max_puntos=MAX_PUNTOS
            )
        except Exception as e:
            print(f"Error al cargar CSV: {e}")
            coordenadas, nombres = None, None

    # Si nada funcionó, generar datos de muestra
    if coordenadas is None:
        print(f"No se pudieron cargar datos desde archivos")
        print(f"Generando dataset de muestra...")
        coordenadas, nombres = processor.crear_dataset_muestra(n_puntos=20)

    # Mostrar estadísticas del dataset
    stats_dataset = processor.obtener_estadisticas()
    print(f"\nEstadísticas del Dataset:")
    print(f"  - Puntos: {stats_dataset['n_puntos']}")
    print(f"  - Latitud: [{stats_dataset['lat_min']:.4f}, {stats_dataset['lat_max']:.4f}]")
    print(f"  - Longitud: [{stats_dataset['lon_min']:.4f}, {stats_dataset['lon_max']:.4f}]")

    # Paso 2: Optimizar rutas
    print(f"\n{'='*70}")
    print(f"CONFIGURACIÓN DE OPTIMIZACIÓN")
    print(f"{'='*70}")
    print(f"Clusters: {N_CLUSTERS}")
    print(f"Método TSP: {METODO_TSP}")
    print(f"{'='*70}\n")

    optimizador = OptimizadorRutasHibrido(n_clusters=N_CLUSTERS)
    resultados = optimizador.optimizar(coordenadas, nombres, metodo_tsp=METODO_TSP)

    # Paso 3: Mostrar ruta
    print(f"\nRUTA OPTIMIZADA:")
    print(f"{'='*70}")
    ruta_nombres = optimizador.obtener_ruta_nombres()
    for i, nombre in enumerate(ruta_nombres[:20], 1):  # Mostrar primeros 20
        print(f"{i:3d}. {nombre}")

    if len(ruta_nombres) > 20:
        print(f"... y {len(ruta_nombres) - 20} puntos más")
    print(f"{'='*70}")

    # Paso 4: Exportar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_json = f'resultados_{timestamp}.json'
    archivo_img = f'clusters_{timestamp}.png'

    optimizador.exportar_resultados(archivo_json)

    # Paso 5: Visualizar
    try:
        visualizar_resultados(coordenadas, nombres, resultados, archivo_img)
    except Exception as e:
        print(f"Error al generar visualización: {e}")

    # Paso 6: Análisis de complejidad
    print(f"\n{'='*70}")
    print(f"ANÁLISIS DE COMPLEJIDAD")
    print(f"{'='*70}")

    n_total = len(coordenadas)

    # Complejidad sin optimización
    print(f"\nSin Optimización (TSP directo sobre {n_total} puntos):")
    if n_total <= 10:
        import math
        print(f"   Complejidad: O({n_total}!) ≈ {math.factorial(n_total):,} operaciones")
        print(f"   Viable con Fuerza Bruta")
    elif n_total <= 15:
        import math
        print(f"   Complejidad: O({n_total}!) ≈ {math.factorial(n_total):,} operaciones")
        print(f"   Viable con Backtracking")
    else:
        print(f"   Complejidad: O({n_total}!) - INTRATABLE")
        print(f"   Imposible con algoritmos exactos")

    # Complejidad con optimización
    print(f"\nCon Optimización Híbrida (K-Means + TSP):")
    print(f"   Clusters: {N_CLUSTERS}")

    tamano_promedio = n_total // N_CLUSTERS
    print(f"   Tamaño promedio de cluster: ~{tamano_promedio} puntos")

    if tamano_promedio <= 10:
        import math
        complejidad_cluster = math.factorial(tamano_promedio)
        print(f"   Complejidad por cluster: O({tamano_promedio}!) ≈ {complejidad_cluster:,} ops")
        print(f"   Complejidad total: O({N_CLUSTERS} × {tamano_promedio}!) ≈ {N_CLUSTERS * complejidad_cluster:,} ops")
    else:
        print(f"   Complejidad: O(n²) con heurística Vecino más Cercano")
        print(f"   ESCALABLE y EFICIENTE")

    print(f"\n{'='*70}")
    print(f"OPTIMIZACIÓN COMPLETADA")
    print(f"{'='*70}")
    print(f"\nArchivos generados:")
    print(f"  - {archivo_json}")
    print(f"  - {archivo_img}")
    print(f"\n¡Listo!")


if __name__ == "__main__":
    main()
