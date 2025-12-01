from tsp_algorithms import resolver_tsp
import numpy as np

def mostrar_menu():
    print("\n" + "="*60)
    print("SISTEMA DE OPTIMIZACION DE RUTAS - ALGORITMOS TSP")
    print("="*60)
    print("\nSeleccione el algoritmo TSP a utilizar:\n")
    print("  1. Fuerza Bruta       - O(n!) - Optimo para n <= 10")
    print("  2. Backtracking       - O(n!) con poda - Optimo para n <= 15")
    print("  3. Vecino mas Cercano - O(n^2) - Heuristico, escalable")
    print("  4. Automatico         - El sistema elige segun el tamano")
    print("  5. Probar todos       - Comparar los 3 algoritmos")
    print("  0. Salir")
    print("\n" + "="*60)

def obtener_opcion():
    while True:
        try:
            opcion = input("\nIngrese su opcion (0-5): ").strip()
            if opcion in ['0', '1', '2', '3', '4', '5']:
                return opcion
            else:
                print("[ERROR] Opcion invalida. Ingrese un numero entre 0 y 5.")
        except KeyboardInterrupt:
            print("\n[INFO] Operacion cancelada por el usuario.")
            return '0'

def ejecutar_tsp(distancias, metodo):
    print(f"\n{'='*60}")
    print(f"[EJECUTANDO] {metodo.upper().replace('_', ' ')}")
    print(f"{'='*60}")

    ruta, distancia, stats = resolver_tsp(distancias, metodo=metodo)

    print(f"\n[RESULTADOS]")
    print(f"  Ruta:           {ruta}")
    print(f"  Distancia:      {distancia:.4f} km")
    print(f"  Metodo usado:   {stats['metodo']}")
    print(f"  Tiempo:         {stats['tiempo']:.6f} segundos")

    if 'permutaciones' in stats:
        print(f"  Permutaciones:  {stats['permutaciones']}")
    if 'nodos_explorados' in stats:
        print(f"  Nodos:          {stats['nodos_explorados']}")
    if 'podas' in stats:
        print(f"  Podas:          {stats['podas']}")

    print(f"{'='*60}")
    return ruta, distancia, stats

def probar_todos(distancias):
    print("\n" + "="*60)
    print("[COMPARACION] Probando todos los algoritmos")
    print("="*60)

    metodos = ['fuerza_bruta', 'backtracking', 'vecino_cercano']
    resultados = []

    for metodo in metodos:
        ruta, distancia, stats = ejecutar_tsp(distancias, metodo)
        resultados.append({
            'metodo': metodo,
            'ruta': ruta,
            'distancia': distancia,
            'tiempo': stats['tiempo']
        })
        input("\n[Presione ENTER para continuar...]")

    # Mostrar comparativa
    print("\n" + "="*60)
    print("[COMPARATIVA FINAL]")
    print("="*60)

    print(f"\n{'Algoritmo':<20} {'Distancia':>12} {'Tiempo (s)':>15}")
    print("-" * 60)
    for r in resultados:
        print(f"{r['metodo']:<20} {r['distancia']:>12.4f} {r['tiempo']:>15.6f}")

    print("\n" + "="*60)

def main():
    # Matriz de distancias de prueba (3 puntos)
    distancias = np.array([
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0]
    ])

    print("\n[INFO] Matriz de distancias cargada (3 puntos)")
    print(distancias)

    while True:
        mostrar_menu()
        opcion = obtener_opcion()

        if opcion == '0':
            print("\n[INFO] Saliendo del sistema...")
            print("="*60)
            break

        elif opcion == '1':
            ejecutar_tsp(distancias, 'fuerza_bruta')

        elif opcion == '2':
            ejecutar_tsp(distancias, 'backtracking')

        elif opcion == '3':
            ejecutar_tsp(distancias, 'vecino_cercano')

        elif opcion == '4':
            ejecutar_tsp(distancias, 'auto')

        elif opcion == '5':
            probar_todos(distancias)

        input("\n[Presione ENTER para volver al menu...]")

if __name__ == '__main__':
    main()
